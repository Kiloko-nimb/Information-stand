// Перечень специальностей ККРИТ.
// Источник: https://kraskrit.ru/abitur/special/
// Добавлены:
//   - subjects: основные изучаемые дисциплины
//   - materials: полезные ссылки и материалы для углубления
//   - hhQuery: поисковый запрос для рынка труда (через /api/v1/market/specialty)

export const specialties = {
  KSK: {
    code: '09.02.01',
    name: 'Компьютерные системы и комплексы',
    qualification: 'Специалист по компьютерным системам',
    duration: '3 года 10 месяцев',
    durationMonths: 46,
    icon: '🖥️',
    accent: '#2563EB',
    summary:
      'Сборка, настройка и обслуживание компьютеров и серверов. ' +
      'Работа со «стальной» частью IT — от железа до низкоуровневых систем.',
    skills: ['Сборка ПК', 'Диагностика техники', 'Настройка ОС', 'Администрирование'],
    subjects: [
      'Архитектура аппаратных средств',
      'Операционные системы и среды',
      'Электротехника и электроника',
      'Технические средства информатизации',
      'Компьютерные сети',
      'Микропроцессорные системы',
      'Программирование на C/C++',
      'Базы данных',
      'Охрана труда',
    ],
    materials: [
      { title: 'Курс «Архитектура компьютера»', source: 'Stepik', url: 'https://stepik.org/course/3134' },
      { title: 'CS50 — основы информатики', source: 'Harvard / edX', url: 'https://cs50.harvard.edu/x/' },
      { title: 'Книга «Современные операционные системы», Э. Таненбаум', source: 'Книга', url: 'https://www.litres.ru/book/endryu-tanenbaum/sovremennye-operacionnye-sistemy/' },
    ],
    hhQuery: 'специалист компьютерных систем',
    url: 'https://kraskrit.ru/abitur/special/',
  },
  SSA: {
    code: '09.02.06',
    name: 'Сетевое и системное администрирование',
    qualification: 'Системный администратор',
    duration: '3 года 10 месяцев',
    durationMonths: 46,
    icon: '🌐',
    accent: '#0EA5B7',
    summary:
      'Настройка локальных сетей, серверов и сервисов. Поддержка ' +
      'инфраструктуры компании, контроль доступов и стабильности систем.',
    skills: ['Linux/Windows Server', 'Cisco', 'Виртуализация', 'Мониторинг'],
    subjects: [
      'Операционные системы (Linux, Windows Server)',
      'Компьютерные сети и протоколы TCP/IP',
      'Сетевое оборудование Cisco / MikroTik',
      'Технологии виртуализации',
      'Администрирование БД (MySQL/PostgreSQL)',
      'Информационная безопасность',
      'Скриптовое программирование (Bash, PowerShell)',
      'Управление IT-инфраструктурой',
    ],
    materials: [
      { title: 'Cisco Networking Academy', source: 'Cisco', url: 'https://www.netacad.com/' },
      { title: 'Курс «Linux для начинающих»', source: 'Stepik', url: 'https://stepik.org/course/73/' },
      { title: 'Книга «Сети для самых маленьких»', source: 'linkmeup', url: 'https://linkmeup.gitbook.io/sdsm/' },
    ],
    hhQuery: 'системный администратор',
    url: 'https://kraskrit.ru/abitur/special/',
  },
  WEB: {
    code: '09.02.09',
    name: 'Веб-разработка',
    qualification: 'Разработчик веб-приложений',
    duration: '2 года 10 месяцев',
    durationMonths: 34,
    icon: '💻',
    accent: '#7C3AED',
    summary:
      'Создание сайтов и веб-приложений: от вёрстки и дизайна до ' +
      'серверной логики и баз данных. Самая «творческая» IT-специальность.',
    skills: ['HTML/CSS/JS', 'Frontend (React/Vue)', 'Backend', 'БД'],
    subjects: [
      'Основы веб-программирования (HTML/CSS)',
      'JavaScript и TypeScript',
      'Frontend-фреймворки (React/Vue)',
      'Backend на Python / Node.js',
      'Базы данных (SQL, NoSQL)',
      'Git и работа в команде',
      'UX/UI дизайн',
      'DevOps и развёртывание приложений',
    ],
    materials: [
      { title: 'HTML Academy — интерактивные курсы', source: 'HTML Academy', url: 'https://htmlacademy.ru/' },
      { title: 'MDN Web Docs', source: 'Mozilla', url: 'https://developer.mozilla.org/ru/' },
      { title: 'Курс «Веб-разработка для начинающих»', source: 'Stepik', url: 'https://stepik.org/course/86290/' },
      { title: 'JavaScript.ru — Современный учебник', source: 'learn.javascript.ru', url: 'https://learn.javascript.ru/' },
    ],
    hhQuery: 'веб разработчик',
    url: 'https://kraskrit.ru/abitur/special/',
    note: 'Платное обучение',
  },
  IB: {
    code: '10.02.05',
    name: 'Обеспечение информационной безопасности',
    qualification: 'Техник по защите информации',
    duration: '3 года 10 месяцев',
    durationMonths: 46,
    icon: '🛡️',
    accent: '#DC2626',
    summary:
      'Защита данных и систем от атак, аудит безопасности, работа ' +
      'с криптографией. «Хорошие хакеры» — те, кто на стороне закона.',
    skills: ['Сетевая безопасность', 'Криптография', 'Аудит', 'Этичный хакинг'],
    subjects: [
      'Основы информационной безопасности',
      'Криптографические методы защиты',
      'Защита персональных данных',
      'Сетевая безопасность',
      'Программно-аппаратные средства защиты',
      'Правовое обеспечение ИБ',
      'Этичный хакинг и пентест',
      'Управление инцидентами',
    ],
    materials: [
      { title: 'TryHackMe — практика безопасности', source: 'TryHackMe', url: 'https://tryhackme.com/' },
      { title: 'Курс «Введение в кибербезопасность»', source: 'Stepik', url: 'https://stepik.org/course/127/' },
      { title: 'Хабр — раздел «Информационная безопасность»', source: 'Habr', url: 'https://habr.com/ru/hub/infosecurity/' },
    ],
    hhQuery: 'специалист информационной безопасности',
    url: 'https://kraskrit.ru/abitur/special/',
  },
  EPU: {
    code: '11.02.16',
    name: 'Электронные приборы и устройства',
    qualification: 'Специалист по электронным приборам и устройствам',
    duration: '3 года 10 месяцев',
    durationMonths: 46,
    icon: '🔧',
    accent: '#F59E0B',
    summary:
      'Монтаж, обслуживание и ремонт электронной техники. Реальная ' +
      'инженерная работа руками — от паяльника до сложных схем.',
    skills: ['Радиоэлектроника', 'Пайка и монтаж', 'Схемотехника', 'Диагностика'],
    subjects: [
      'Электротехника и электронная техника',
      'Аналоговая и цифровая схемотехника',
      'Микроконтроллеры (Arduino, STM32)',
      'Монтаж и пайка электронных устройств',
      'Метрология и измерительная техника',
      'Системы автоматики',
      'Технология производства РЭА',
      'Охрана труда',
    ],
    materials: [
      { title: 'Arduino: первые шаги', source: 'Amperka', url: 'https://wiki.amperka.ru/' },
      { title: 'Курс «Электроника для начинающих»', source: 'Stepik', url: 'https://stepik.org/course/56192/' },
      { title: 'Книга «Искусство схемотехники», Хоровиц/Хилл', source: 'Книга', url: 'https://www.litres.ru/book/pol-horovic/iskusstvo-shemotehniki-tom-1/' },
    ],
    hhQuery: 'инженер электроник',
    url: 'https://kraskrit.ru/abitur/special/',
  },
  EBU: {
    code: '38.02.01',
    name: 'Экономика и бухгалтерский учёт',
    qualification: 'Бухгалтер',
    duration: '2 года 10 месяцев',
    durationMonths: 34,
    icon: '📊',
    accent: '#059669',
    summary:
      'Учёт и анализ финансов компании, налогообложение, отчётность. ' +
      'Точная работа с цифрами и документами.',
    skills: ['1С: Бухгалтерия', 'Налоговый учёт', 'Финансовый анализ', 'Excel'],
    subjects: [
      'Основы бухгалтерского учёта',
      'Налоги и налогообложение',
      'Финансы организаций',
      'Аудит',
      '1С: Бухгалтерия 8.3',
      'Экономика организации',
      'Статистика',
      'Документационное обеспечение',
    ],
    materials: [
      { title: 'Курс «1С: Бухгалтерия для начинающих»', source: '1С', url: 'https://its.1c.ru/db/edu' },
      { title: 'Налоговый кодекс РФ — справочник', source: 'КонсультантПлюс', url: 'https://www.consultant.ru/document/cons_doc_LAW_19671/' },
      { title: 'Бухгалтерия.ру — журнал', source: 'Buhgalteria.ru', url: 'https://www.buhgalteria.ru/' },
    ],
    hhQuery: 'бухгалтер',
    url: 'https://kraskrit.ru/abitur/special/',
  },
  BD: {
    code: '38.02.07',
    name: 'Банковское дело',
    qualification: 'Специалист банковского дела',
    duration: '2 года 10 месяцев',
    durationMonths: 34,
    icon: '🏦',
    accent: '#0891B2',
    summary:
      'Работа в банковской сфере: кредитование, операционное обслуживание, ' +
      'инвестиции, цифровые финансовые сервисы.',
    skills: ['Банковские продукты', 'Кредитование', 'Финтех', 'Клиентский сервис'],
    subjects: [
      'Банковские операции',
      'Кредитование физических и юридических лиц',
      'Финансовый менеджмент',
      'Рынок ценных бумаг',
      'Цифровые финансовые услуги',
      'Банковский маркетинг',
      'Финансовая математика',
      'Деловое общение',
    ],
    materials: [
      { title: 'Финансовая грамотность — учебный курс', source: 'ЦБ РФ', url: 'https://fincult.info/' },
      { title: 'Курс «Введение в финансы»', source: 'Stepik', url: 'https://stepik.org/course/2724/' },
      { title: 'Сбер про — образовательный портал', source: 'Сбер', url: 'https://www.sberbank.ru/promo/sber-pro/' },
    ],
    hhQuery: 'специалист банка',
    url: 'https://kraskrit.ru/abitur/special/',
  },
}

export const specialtyList = Object.entries(specialties).map(([key, data]) => ({ key, ...data }))
