from apscheduler.schedulers.background import BackgroundScheduler # type: ignore
from django.db.models.functions import ExtractMonth, ExtractDay
from django.utils import timezone
import random
from users.models import User
from core.utils.send_email import send_email
from core.utils.email_html import EmailHtmlContent

def send_birthday_emails():
    today = timezone.now().date()
    users = User.objects.annotate(
        birth_month=ExtractMonth('dateOfBirth'),
        birth_day=ExtractDay('dateOfBirth')
    ).filter(
        birth_month=today.month,
        birth_day=today.day
    )

    BIRTHDAY_MESSAGES = [
        "Wishing you a day filled with love, laughter, and the warmth of those who cherish you. May this special day mark the beginning of a year filled with new opportunities, great achievements, and cherished moments that bring you endless happiness. Celebrate today knowing you are deeply valued and appreciated!",
        
        "Happy Birthday! May your journey ahead be filled with boundless joy, exciting adventures, and beautiful memories. As you step into another year, may you continue to inspire those around you with your kindness, strength, and wisdom. Enjoy every moment of your special day, for you truly deserve it!",
        
        "On your birthday, I wish you not only success and good health but also peace of mind, deep fulfillment, and happiness that lasts a lifetime. May today be the beginning of a fantastic new chapter where your dreams take flight and your aspirations turn into reality. Have a fantastic celebration!",
        
        "As you celebrate your birthday today, may you be surrounded by love, laughter, and positivity. May this new year of your life bring you closer to your dreams, fill your heart with joy, and grant you the courage to chase your passions. May your light continue to shine brightly in the world!",
        
        "Another year older, another year wiser! On your special day, may you reflect on all the beautiful moments of the past and look forward to an even brighter future. May your heart always be full of love, your soul at peace, and your life filled with endless joy. Have a birthday as wonderful as you are!",
        
        "Today, we celebrate you—your kindness, your dreams, and the unique spark that makes you who you are. May your birthday be filled with heartfelt moments, sweet surprises, and all the happiness you bring to others. Wishing you a spectacular year ahead, full of success, love, and everything you desire!",
        
        "May your birthday be filled with endless laughter, treasured memories, and the presence of those who make your heart smile. Life is a journey, and you have already accomplished so much. May this year bring new opportunities, incredible adventures, and boundless happiness. Have a beautiful birthday!",
        
        "On this special day, I want to remind you how incredibly special you are. You bring light, love, and joy into the lives of so many. May your birthday be a reflection of the kindness you show the world—a day filled with love, appreciation, and all the things that make you happiest. Cheers to a bright future ahead!",
        
        "Birthdays are not just about celebrating another year; they are about cherishing the moments, embracing growth, and looking forward to the future with hope and excitement. May today be filled with laughter, love, and the presence of those who truly appreciate you. Wishing you the best year yet!",
        
        "On your birthday, take a moment to appreciate how far you've come, the lessons you've learned, and the lives you've touched. You are an incredible person, and the world is a better place because of you. May your new year be filled with boundless love, great opportunities, and unforgettable moments!",
        
        "Today is all about you, and you deserve nothing but the best! May your heart be filled with gratitude, your soul with peace, and your days with happiness. May you continue to inspire and shine, and may all your dreams unfold beautifully in the year ahead. Have a birthday as wonderful as your spirit!",
        
        "As you celebrate another year of life, may you be blessed with good health, unshakable happiness, and countless cherished moments. Your kindness and strength make the world a brighter place. May this birthday mark the beginning of an incredible journey filled with success and fulfillment!",
        
        "A birthday is not just about growing older; it’s about growing wiser, stronger, and more grateful for life’s blessings. On your special day, may you feel loved, appreciated, and inspired. May the year ahead bring you closer to your dreams and fill your life with beautiful surprises. Have a fantastic birthday!",
        
        "May today bring you joy, reflection, and a heart full of gratitude. You have touched so many lives with your kindness and wisdom. May this new chapter be filled with success, adventure, and everything that makes your heart sing. Wishing you a birthday as amazing as you are!",
        
        "Happy Birthday to someone truly wonderful! May this year bring you immense happiness, good health, and prosperity. May your journey ahead be filled with beautiful moments and loving relationships. Celebrate today knowing you are cherished and deeply valued. Have a fantastic birthday!",
        
        "On this special day, I wish you moments of joy, deep conversations, and beautiful memories that will last a lifetime. May you continue to inspire and bring light into the lives of those around you. May today be filled with laughter, love, and everything you hold dear!",
        
        "Birthdays are a time to celebrate, reflect, and look forward to new possibilities. May your life continue to be a wonderful adventure filled with love, laughter, and success. Embrace the journey ahead with courage and excitement. Have a spectacular birthday!",
        
        "Happy Birthday! May this new year bring you closer to your dreams and fill your heart with joy. Remember that every day is an opportunity to create, inspire, and achieve. May you be blessed with everything that makes life meaningful—love, friendship, and endless happiness!",
        
        "Today, I celebrate you—the person you are and the incredible journey ahead. May this birthday remind you of how special and loved you are. May you find happiness in the little things, strength in challenges, and endless love in the people who matter most. Wishing you the happiest birthday yet!",
        
        "May your birthday be a day of joy, love, and gratitude. You have accomplished so much, and your future holds even greater things. May this be the start of a year filled with blessings, exciting opportunities, and wonderful surprises. Celebrate your journey, for you are truly remarkable!"
    ]

    for user in users:
        message = random.choice(BIRTHDAY_MESSAGES)
        html_body = EmailHtmlContent.generate_html(user.firstName, message=message)

        send_email(
            recipient_email=user.username,
            recipient_name=user.firstName,
            subject="Best Wishes on Your Birthday!🎂🎈",
            html_content=html_body
        )

    print(f"Birthday emails sent for {today}.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_birthday_emails, "interval", minutes=720)
    scheduler.start()