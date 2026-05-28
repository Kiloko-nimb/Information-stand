// Словари переводов для интерфейса стенда.
// Не покрывают 100% — фокус на самых заметных строках главного экрана,
// абитуриентских разделов и навигации. Динамика (новости, расписание) остаётся
// на русском, так как идёт из БД.

export const messages = {
  ru: {
    nav: {
      home: 'Главная',
      schedule: 'Расписание',
      staff: 'Преподаватели',
      map: 'Карта',
      faq: 'Вопросы',
      quiz: 'Тест профессии',
    },
    roles: {
      student: 'Студент',
      applicant: 'Абитуриент',
      teacher: 'Преподаватель',
    },
    home: {
      news: 'Свежие новости',
      allNews: 'Все новости →',
      bells: 'Расписание звонков',
      now: 'Сейчас',
      next: 'Следующая',
      break: 'Перемена',
    },
    applicant: {
      title: 'Абитуриенту 2026',
      passingScores: 'Проходные баллы',
      specialties: 'Специальности',
      compare: 'Сравнить специальности',
      quiz: 'Подобрать профессию',
      calculator: 'Калькулятор шансов',
      apply: 'Подать заявление',
    },
    common: {
      back: 'На главную',
      details: 'Подробнее',
      loading: 'Загрузка…',
      noData: 'Нет данных',
      seeAll: 'Все',
    },
  },
  en: {
    nav: {
      home: 'Home',
      schedule: 'Schedule',
      staff: 'Staff',
      map: 'Map',
      faq: 'FAQ',
      quiz: 'Career test',
    },
    roles: {
      student: 'Student',
      applicant: 'Applicant',
      teacher: 'Teacher',
    },
    home: {
      news: 'Latest news',
      allNews: 'All news →',
      bells: 'Bell schedule',
      now: 'Now',
      next: 'Next',
      break: 'Break',
    },
    applicant: {
      title: 'Applicant 2026',
      passingScores: 'Passing scores',
      specialties: 'Specialties',
      compare: 'Compare specialties',
      quiz: 'Find your career',
      calculator: 'Admission calculator',
      apply: 'Apply',
    },
    common: {
      back: 'Home',
      details: 'Details',
      loading: 'Loading…',
      noData: 'No data',
      seeAll: 'All',
    },
  },
}

export const AVAILABLE_LOCALES = [
  { id: 'ru', name: 'Русский', short: 'РУ' },
  { id: 'en', name: 'English', short: 'EN' },
]
