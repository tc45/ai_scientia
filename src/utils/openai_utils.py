from django.conf import settings
from openai import OpenAI
import logging
import time
from typing import Dict, Optional, Any

logger = logging.getLogger(__name__)

class OpenAIContentGenerator:
    """Utility class for generating content using OpenAI's API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenAI content generator
        
        Args:
            api_key: Optional OpenAI API key. If not provided, will use settings.OPENAI_API_KEY
        """
        self.api_key = api_key or settings.OPENAI_API_KEY
        if not self.api_key:
            logger.warning("No OpenAI API key provided. Content generation will be disabled.")
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
        
    def generate_content(
        self,
        prompt_template: str,
        variables: Dict[str, Any],
        model: str = "gpt-3.5-turbo",
        max_retries: int = 3,
        retry_delay: int = 1,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        Generate content using OpenAI's API with retry logic
        """
        if not self.client:
            logger.error("Cannot generate content: No OpenAI API key provided")
            return None
        
        # Format the prompt with provided variables
        try:
            prompt = prompt_template.format(**variables)
        except KeyError as e:
            logger.error(f"Missing variable in prompt template: {e}")
            return None
        
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a professional blog writer with expertise in technology and AI."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                if response.choices and response.choices[0].message:
                    return response.choices[0].message.content.strip()
                    
            except Exception as e:
                logger.warning(f"OpenAI API error (attempt {attempt + 1}/{max_retries}): {e}")
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                continue
                
        logger.error("All retry attempts failed")
        return None

    def generate_blog_post(
        self,
        title: str,
        topic: str,
        excerpt_length: int = 200
    ) -> Dict[str, str]:
        """
        Generate a complete blog post with title, content, and excerpt
        """
        prompt_template = """Create a comprehensive blog post on {title} with a focus on {topic}.

Please structure the post as follows:
1. Introduction: Set the context and explain why this topic matters
2. 2-5 main content sections with relevant subheadings
3. Conclusion: Summarize key points and provide future outlook

Use markdown formatting for headings and sections.
Keep the tone professional but engaging.
Include practical examples and applications where relevant."""

        content = self.generate_content(
            prompt_template=prompt_template,
            variables={'title': title, 'topic': topic},
            temperature=0.7
        )
        
        if not content:
            return {'content': '', 'excerpt': ''}
            
        # Generate a shorter excerpt
        excerpt_prompt = f"Create a compelling {excerpt_length}-character excerpt summarizing the following blog post: {title}"
        excerpt = self.generate_content(
            prompt_template=excerpt_prompt,
            variables={},
            max_tokens=100,
            temperature=0.5
        )
        
        return {
            'content': content,
            'excerpt': excerpt[:excerpt_length] if excerpt else ''
        } 