// Доска почёта / Аллея славы ККРИТ.
// Данные пока заглушечные — заполнить реальными достижениями студентов.
// Поле photo может быть либо URL картинкой, либо null (тогда будут инициалы).

export const honorCategories = [
  { id: 'all', label: 'Все', icon: '⭐' },
  { id: 'hackathon', label: 'Хакатоны', icon: '💻' },
  { id: 'olympiad', label: 'Олимпиады', icon: '🏆' },
  { id: 'profskills', label: 'WorldSkills', icon: '🛠️' },
  { id: 'science', label: 'Научные конференции', icon: '🔬' },
  { id: 'esports', label: 'Киберспорт', icon: '🎮' },
  { id: 'sport', label: 'Спорт', icon: '🥇' },
]

export const honorEntries = [
  {
    id: 'h1',
    name: 'Иванов Иван Иванович',
    group: 'ИС-22',
    year: 2025,
    category: 'hackathon',
    achievement: '1 место в региональном хакатоне «Цифровой Красноярск»',
    description:
      'Команда разработала прототип сервиса для ускорения записи в МФЦ — победили из 38 команд.',
    photo: null,
    accent: '#2563EB',
  },
  {
    id: 'h2',
    name: 'Петрова Анна Сергеевна',
    group: 'СА-21',
    year: 2025,
    category: 'profskills',
    achievement: 'Золото WorldSkills Russia, компетенция «Сетевое и системное администрирование»',
    description:
      'Лучший результат среди СПО Красноярского края, прошла в национальный финал.',
    photo: null,
    accent: '#0EA5B7',
  },
  {
    id: 'h3',
    name: 'Сидоров Дмитрий Алексеевич',
    group: 'ИБ-23',
    year: 2025,
    category: 'olympiad',
    achievement: '2 место во Всероссийской олимпиаде по информационной безопасности',
    description:
      'Решил все задачи на криптоанализ и сетевую защиту, не хватило одной задачи на форензику.',
    photo: null,
    accent: '#DC2626',
  },
  {
    id: 'h4',
    name: 'Кузнецова Мария Олеговна',
    group: 'ВЕБ-22',
    year: 2024,
    category: 'hackathon',
    achievement: 'Победитель IT-марафона «КодКодКод-2024»',
    description: 'Авторский веб-сервис для подачи заявлений в студсовет, ушёл в продакшн колледжа.',
    photo: null,
    accent: '#7C3AED',
  },
  {
    id: 'h5',
    name: 'Команда «KKRIT.eSports»',
    group: 'Сборная колледжа',
    year: 2025,
    category: 'esports',
    achievement: 'Чемпионы Красноярского края по Counter-Strike 2 среди СПО',
    description: 'Финал прошёл всухую 16:6, состав смешанный из 3 групп.',
    photo: null,
    accent: '#F59E0B',
  },
  {
    id: 'h6',
    name: 'Орлов Никита Романович',
    group: 'ЭПУ-22',
    year: 2024,
    category: 'science',
    achievement: 'Лучший доклад на студенческой конференции «Молодёжь и наука»',
    description: 'Тема — автономный модуль контроля микроклимата серверной на ESP32.',
    photo: null,
    accent: '#059669',
  },
  {
    id: 'h7',
    name: 'Лебедева Ксения Игоревна',
    group: 'ЭБУ-21',
    year: 2025,
    category: 'sport',
    achievement: 'КМС по плаванию, призёр первенства Сибири',
    description: 'Совмещает учёбу и спорт высоких достижений, тренируется 6 раз в неделю.',
    photo: null,
    accent: '#0891B2',
  },
  {
    id: 'h8',
    name: 'Громов Артём Викторович',
    group: 'СА-20',
    year: 2024,
    category: 'profskills',
    achievement: 'Серебро национального финала WorldSkills, компетенция «Кибербезопасность»',
    description: 'Лучший представитель Красноярского края, после колледжа работает в крупной IT-компании.',
    photo: null,
    accent: '#0E7490',
  },
  {
    id: 'h9',
    name: 'Смирнова Полина Дмитриевна',
    group: 'ИС-22',
    year: 2025,
    category: 'hackathon',
    achievement: '3 место на Open Hack Day, г. Новосибирск',
    description: 'AI-чатбот-помощник для абитуриентов СПО — сейчас тестируется в колледже.',
    photo: null,
    accent: '#7C3AED',
  },
  {
    id: 'h10',
    name: 'Команда «KKRIT-Algo»',
    group: 'Сборная колледжа',
    year: 2024,
    category: 'olympiad',
    achievement: 'Финалисты ICPC Sibirian Subregional Contest',
    description: '14 место среди вузов и СПО Сибирского федерального округа.',
    photo: null,
    accent: '#2563EB',
  },
]

export function getInitials(fullName) {
  if (!fullName) return '??'
  const parts = fullName.trim().split(/\s+/)
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase()
  return (parts[0][0] + parts[1][0]).toUpperCase()
}
