from random import choice
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned


from datacenter.models import (
    Mark,
    Chastisement,
    Schoolkid,
    Commendation,
    Lesson
)


def find_schoolkid(schoolkid):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except ObjectDoesNotExist:
        print('Нет такого ученика')
    except MultipleObjectsReturned:
        print('Таких учеников несколько')


def fix_marks(schoolkid):
    customer = find_schoolkid(schoolkid)
    if customer:
        bad_marks = Mark.objects.filter(schoolkid=customer, points__in=[1, 2, 3])
        for mark in bad_marks:
            mark.points = 5
            mark.save()


def remove_chastisements(schoolkid):
    customer = find_schoolkid(schoolkid)
    if customer:
        chastisement = Chastisement.objects.filter(schoolkid=customer)
        chastisement.delete()


def create_commendation(schoolkid, subject):
    commendations = ['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                     'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                     'Сказано здорово – просто и ясно!', 'Ты, как всегда, точен!', 'Очень хороший ответ!',
                     'Талантливо!', 'Ты сегодня прыгнул выше головы!', 'Я поражен!', 'Уже существенно лучше!',
                     'Потрясающе!', 'Замечательно!', 'Прекрасное начало!', 'Так держать!', 'Ты на верном пути!',
                     'Здорово!', 'Это как раз то, что нужно!', 'Я тобой горжусь!',
                     'С каждым разом у тебя получается всё лучше!', 'Мы с тобой не зря поработали!',
                     'Я вижу, как ты стараешься!', 'Ты растешь над собой!', 'Ты многое сделал, я это вижу!',
                     'Теперь у тебя точно все получится!']
    commendation = choice(commendations)
    lessons = Lesson.objects.filter(
        year_of_study=6,
        group_letter='А',
        subject__title=subject
    )
    lesson = lessons[lessons.count() // 2]
    customer = find_schoolkid(schoolkid)
    if customer:
        Commendation.objects.create(
            text=commendation,
            created=lesson.date,
            schoolkid=customer,
            subject=lesson.subject,
            teacher=lesson.teacher
        )
