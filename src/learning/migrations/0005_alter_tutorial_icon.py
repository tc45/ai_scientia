# Generated by Django 5.0.2 on 2025-01-12 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("learning", "0004_tutorial_icon"),
    ]

    operations = [
        migrations.AlterField(
            model_name="tutorial",
            name="icon",
            field=models.CharField(
                choices=[
                    ("fas fa-robot", "Robot"),
                    ("fas fa-brain", "Brain"),
                    ("fas fa-microchip", "Microchip"),
                    ("fas fa-network-wired", "Neural Network"),
                    ("fas fa-project-diagram", "Neural Connections"),
                    ("fas fa-sitemap", "Deep Learning"),
                    ("fas fa-code", "Code"),
                    ("fas fa-laptop-code", "Laptop with Code"),
                    ("fas fa-terminal", "Terminal"),
                    ("fas fa-bug", "Debug"),
                    ("fas fa-file-code", "Code File"),
                    ("fas fa-keyboard", "Keyboard"),
                    ("fas fa-database", "Database"),
                    ("fas fa-server", "Server"),
                    ("fas fa-chart-line", "Analytics Graph"),
                    ("fas fa-chart-bar", "Bar Chart"),
                    ("fas fa-chart-pie", "Pie Chart"),
                    ("fas fa-table", "Data Table"),
                    ("fas fa-cloud", "Cloud"),
                    ("fas fa-cloud-upload-alt", "Cloud Upload"),
                    ("fas fa-cloud-download-alt", "Cloud Download"),
                    ("fas fa-server", "Server"),
                    ("fas fa-hdd", "Storage"),
                    ("fas fa-memory", "Memory"),
                    ("fas fa-shield-alt", "Security Shield"),
                    ("fas fa-lock", "Lock"),
                    ("fas fa-key", "Key"),
                    ("fas fa-user-shield", "User Security"),
                    ("fas fa-fingerprint", "Biometric"),
                    ("fas fa-tools", "Tools"),
                    ("fas fa-cogs", "Settings Gears"),
                    ("fas fa-wrench", "Wrench"),
                    ("fas fa-sliders-h", "Sliders"),
                    ("fas fa-toolbox", "Toolbox"),
                    ("fas fa-graduation-cap", "Education"),
                    ("fas fa-book", "Book"),
                    ("fas fa-chalkboard-teacher", "Teaching"),
                    ("fas fa-user-graduate", "Graduate"),
                    ("fas fa-pencil-alt", "Writing"),
                    ("fas fa-microphone", "Voice/Audio"),
                    ("fas fa-camera", "Computer Vision"),
                    ("fas fa-language", "NLP"),
                    ("fas fa-comments", "Chatbot"),
                    ("fas fa-vr-cardboard", "Virtual Reality"),
                    ("fas fa-gamepad", "Gaming AI"),
                ],
                default="fas fa-book",
                help_text="FontAwesome icon class",
                max_length=50,
            ),
        ),
    ]
