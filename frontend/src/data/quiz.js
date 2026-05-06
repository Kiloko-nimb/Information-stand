// Тест профориентации «Какая IT-профессия тебе подойдёт?»
// Каждый ответ начисляет баллы одной или нескольким специальностям.
// Ключи специальностей соответствуют объекту `specialties` в ./specialties.js.

export const quizQuestions = [
  {
    id: 'q1',
    text: 'Что тебе больше всего нравится делать с компьютером?',
    options: [
      {
        id: 'q1a',
        label: 'Собирать или чинить технику, разбираться, как она устроена',
        scores: { KSK: 3, EPU: 2 },
      },
      {
        id: 'q1b',
        label: 'Настраивать сети, серверы, общие папки и принтеры',
        scores: { SSA: 3, KSK: 1 },
      },
      {
        id: 'q1c',
        label: 'Делать сайты, писать код, видеть результат в браузере',
        scores: { WEB: 3, KSK: 1 },
      },
      {
        id: 'q1d',
        label: 'Защищать данные, искать уязвимости, работать с шифрованием',
        scores: { IB: 3, SSA: 1 },
      },
      {
        id: 'q1e',
        label: 'Работать с цифрами, отчётами, финансами',
        scores: { EBU: 3, BD: 2 },
      },
    ],
  },
  {
    id: 'q2',
    text: 'Какая часть айтишного мира тебя сильнее зажигает?',
    options: [
      {
        id: 'q2a',
        label: 'Внутренности компьютеров, серверов и плат',
        scores: { KSK: 2, EPU: 2 },
      },
      {
        id: 'q2b',
        label: 'Сети, протоколы, маршрутизация',
        scores: { SSA: 3 },
      },
      {
        id: 'q2c',
        label: 'Сайты, мобильные приложения, интерфейсы',
        scores: { WEB: 3 },
      },
      {
        id: 'q2d',
        label: 'Кибербезопасность, антивирусы, расследования',
        scores: { IB: 3 },
      },
      {
        id: 'q2e',
        label: 'Финтех, банковские приложения, цифровые деньги',
        scores: { BD: 3, EBU: 1 },
      },
    ],
  },
  {
    id: 'q3',
    text: 'Чем ты, скорее всего, занимаешься в свободное время?',
    options: [
      {
        id: 'q3a',
        label: 'Разбираю старую электронику, паяю, собираю свой ПК',
        scores: { EPU: 3, KSK: 1 },
      },
      {
        id: 'q3b',
        label: 'Играю по сети, общаюсь в Discord, помогаю друзьям с настройкой',
        scores: { SSA: 2, WEB: 1 },
      },
      {
        id: 'q3c',
        label: 'Пишу код, делаю свои pet-проекты, изучаю фреймворки',
        scores: { WEB: 3 },
      },
      {
        id: 'q3d',
        label: 'Читаю про взломы, CTF и кибербезопасность',
        scores: { IB: 3 },
      },
      {
        id: 'q3e',
        label: 'Слежу за курсом валют, изучаю инвестиции',
        scores: { EBU: 2, BD: 2 },
      },
    ],
  },
  {
    id: 'q4',
    text: 'Что тебе важнее в будущей работе?',
    options: [
      {
        id: 'q4a',
        label: 'Работать руками с реальными устройствами',
        scores: { EPU: 3, KSK: 1 },
      },
      {
        id: 'q4b',
        label: 'Держать всё под контролем — серверы, доступы, инфраструктуру',
        scores: { SSA: 2, IB: 2 },
      },
      {
        id: 'q4c',
        label: 'Видеть результат своей работы у пользователей',
        scores: { WEB: 3 },
      },
      {
        id: 'q4d',
        label: 'Защищать людей и компании от киберугроз',
        scores: { IB: 3 },
      },
      {
        id: 'q4e',
        label: 'Работать со стабильным графиком и хорошей зарплатой',
        scores: { EBU: 2, BD: 2 },
      },
    ],
  },
  {
    id: 'q5',
    text: 'Какой результат принесёт тебе больше удовольствия?',
    options: [
      {
        id: 'q5a',
        label: 'Работающий компьютер, который ты собрал и настроил',
        scores: { KSK: 3, EPU: 1 },
      },
      {
        id: 'q5b',
        label: 'Стабильная сеть, в которой все сервисы работают без сбоев',
        scores: { SSA: 3 },
      },
      {
        id: 'q5c',
        label: 'Запущенный сайт или приложение, которым пользуются люди',
        scores: { WEB: 3 },
      },
      {
        id: 'q5d',
        label: 'Предотвращённая атака или закрытая уязвимость',
        scores: { IB: 3 },
      },
      {
        id: 'q5e',
        label: 'Сбалансированный отчёт и довольный клиент',
        scores: { EBU: 2, BD: 2 },
      },
    ],
  },
]

export function calculateQuizResult(answers) {
  // answers: { q1: 'q1a', q2: 'q2c', ... }
  const totals = {}

  for (const question of quizQuestions) {
    const answerId = answers[question.id]
    if (!answerId) continue
    const option = question.options.find((o) => o.id === answerId)
    if (!option) continue
    for (const [key, score] of Object.entries(option.scores)) {
      totals[key] = (totals[key] || 0) + score
    }
  }

  const ranked = Object.entries(totals)
    .sort((a, b) => b[1] - a[1])
    .map(([key, score]) => ({ key, score }))

  return {
    ranked,
    primary: ranked[0]?.key || null,
    secondary: ranked[1]?.key || null,
    totals,
  }
}
