<template>
  <div class="map-floor">
    <div class="map-header">
      <h2>1 этаж</h2>
    </div>

    <div class="map-container">
      <svg
        width="1005.8719"
        height="379.78632"
        viewBox="0 0 1005.8719 379.7863"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        @click="handleSvgClick"
      >
        <defs>
          <!-- Точечный фон коридоров — снимает белизну чертёжной заливки. -->
          <pattern id="bg-dots-1" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
            <rect width="22" height="22" fill="#f8fafc"/>
            <circle cx="11" cy="11" r="1" fill="#cbd5e1" opacity="0.65"/>
          </pattern>
          <!-- Лёгкая тень под комнатами для объёма. -->
          <filter id="room-shadow-1" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08"/>
          </filter>
        </defs>

        <rect x="0" y="0" width="1005.8719" height="379.7863" fill="url(#bg-dots-1)"/>

        <g transform="translate(-42.677711,-584.16905)">
          <!-- Стены, двери и прочая графика из исходного Inkscape-файла. -->
<line x1="500.7645" y1="585.41907" x2="572.76447" y2="585.41907" stroke="#1a1a1a" stroke-width="2.5" id="line1" style="display:inline" clip-path="none"/>
          <path d="m 570.7645,586.66905 v 99.99999 h 325 v 190 h -700 v -190 h 305 v -99.99999 z" stroke="#1a1a1a" stroke-width="5" stroke-linecap="square" id="path1" style="display:inline" clip-path="none"/>
          <path d="m 315.7645,756.66904 h 185" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path11" style="display:inline" clip-path="none"/>
          <path d="M 501.82066,756.46454 H 755.29959" stroke="#1a1a1a" stroke-width="2.92634" stroke-linecap="square" id="path12" style="display:inline" clip-path="none"/>
          <path d="m 421.34002,686.39638 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path14" style="display:inline" clip-path="none"/>
          <path d="m 501.34002,686.39638 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path15" style="display:inline" clip-path="none"/>
          <path d="m 640.7645,686.66904 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path21" style="display:inline" clip-path="none"/>
          <path d="m 703.7645,685.66904 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path22" style="display:inline" clip-path="none"/>
          <path d="m 757.6726,686.45889 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path22-2" style="display:inline" clip-path="none"/>
          <path d="m 823.79599,685.83421 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path22-2-1" style="display:inline" clip-path="none"/>
          <path d="m 856.2645,685.54835 v 49.24138" stroke="#1a1a1a" stroke-width="2.0968" stroke-linecap="square" id="path22-2-1-4" style="display:inline" clip-path="none"/>
          <path d="m 844.88579,735.12279 h 22.71772" stroke="#1a1a1a" stroke-width="1.42421" stroke-linecap="square" id="path22-2-1-4-0" style="display:inline" clip-path="none"/>
          <path d="M 844.77296,756.59306 V 735.16922" stroke="#1a1a1a" stroke-width="1.38306" stroke-linecap="square" id="path22-2-1-4-0-6" style="display:inline" clip-path="none"/>
          <path d="M 867.64353,756.53441 V 735.11057" stroke="#1a1a1a" stroke-width="1.38306" stroke-linecap="square" id="path22-2-1-4-0-6-8" style="display:inline" clip-path="none"/>
          <path d="m 703.1636,804.27983 v 69.74404" stroke="#1a1a1a" stroke-width="2.49543" stroke-linecap="square" id="path22-2-1-7" style="display:inline" clip-path="none"/>
          <path d="m 641.16103,804.18639 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path22-2-1-7-1" style="display:inline" clip-path="none"/>
          <path d="m 556.07866,833.50759 v 41.51848" stroke="#1a1a1a" stroke-width="1.92536" stroke-linecap="square" id="path22-2-1-7-1-1" style="display:inline" clip-path="none"/>
          <path d="m 598.48607,833.50714 v 41.51848" stroke="#1a1a1a" stroke-width="1.92536" stroke-linecap="square" id="path22-2-1-7-1-1-3" style="display:inline" clip-path="none"/>
          <path d="M 703.107,804.19875 H 641.0859" stroke="#1a1a1a" stroke-width="2.35321" stroke-linecap="square" id="path22-2-1-7-1-5" style="display:inline" clip-path="none"/>
          <path d="m 764.86804,804.25604 v 69.74404" stroke="#1a1a1a" stroke-width="2.49543" stroke-linecap="square" id="path22-2-1-7-6" style="display:inline" clip-path="none"/>
          <path d="m 764.81144,804.17496 h -62.0211" stroke="#1a1a1a" stroke-width="2.35321" stroke-linecap="square" id="path22-2-1-7-1-5-1" style="display:inline" clip-path="none"/>
          <path d="M 597.46957,833.51541 H 556.06718" stroke="#1a1a1a" stroke-width="1.92267" stroke-linecap="square" id="path22-2-1-7-1-5-4" style="display:inline" clip-path="none"/>
          <path d="m 755.7645,756.66904 h 140" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path23" style="display:inline" clip-path="none"/>
          <path d="m 381.12717,756.82877 h 15" stroke="#fcfcfc" stroke-width="7" id="path37" style="display:inline" clip-path="none"/>
          <path d="m 610.61026,756.47624 h 15" stroke="#fcfcfc" stroke-width="7" id="path43" style="display:inline" clip-path="none"/>
          <path d="m 508.96194,756.42083 h 15" stroke="#fcfcfc" stroke-width="7" id="path43-8" style="display:inline" clip-path="none"/>
          <path d="M 608.15846,876.36582 H 626.8217" stroke="#fcfcfc" stroke-width="7.80811" id="path43-8-9" style="display:inline" clip-path="none"/>
          <path d="m 598.47198,844.81099 v 18.66324" stroke="#fcfcfc" stroke-width="7.80811" id="path43-8-9-1" style="display:inline" clip-path="none"/>
          <path d="m 531.71999,876.27473 h 18.66324" stroke="#fcfcfc" stroke-width="7.80811" id="path43-8-9-7" style="display:inline" clip-path="none"/>
          <path d="m 721.61283,757.24745 h 15" stroke="#fcfcfc" stroke-width="7" id="path44" style="display:inline" clip-path="none"/>
          <path d="m 320.2645,755.66904 h 15" stroke="#fcfcfc" stroke-width="7" id="path49" style="display:inline" clip-path="none"/>
          <path d="m 461.68085,686.53271 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path52" style="display:inline" clip-path="none"/>
          <path d="m 357.61219,685.79693 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path52-1" style="display:inline" clip-path="none"/>
          <path d="m 421.34002,691.39638 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40" stroke="#1a1a1a" stroke-width="1.5" id="path53" style="display:inline" clip-path="none"/>
          <path d="m 461.34002,691.39638 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40" stroke="#1a1a1a" stroke-width="1.5" id="path54" style="display:inline" clip-path="none"/>
          <path d="m 672.2645,686.66904 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path55" style="display:inline" clip-path="none"/>
          <path d="m 641.7645,691.66904 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30" stroke="#1a1a1a" stroke-width="1.5" id="path56" style="display:inline" clip-path="none"/>
          <path d="m 672.7645,691.66904 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30" stroke="#1a1a1a" stroke-width="1.5" id="path57" style="display:inline" clip-path="none"/>
          <path d="m 195.7645,706.66904 v 30" stroke="#1a1a1a" id="path66" style="display:inline" clip-path="none"/>
          <path d="m 895.7645,821.66904 v 30" stroke="#1a1a1a" id="path77" style="display:inline" clip-path="none"/>
          <path d="m 270.7645,683.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path78" style="display:inline" clip-path="none"/>
          <path d="m 240.7645,686.66904 h 30" stroke="#1a1a1a" id="path79" style="display:inline" clip-path="none"/>
          <path d="m 350.7645,683.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path80" style="display:inline" clip-path="none"/>
          <path d="m 320.7645,686.66904 h 30" stroke="#1a1a1a" id="path81" style="display:inline" clip-path="none"/>
          <path d="m 632.80306,684.44025 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path82" style="display:inline" clip-path="none"/>
          <path d="m 602.80306,687.44025 h 30" stroke="#1a1a1a" id="path83" style="display:inline" clip-path="none"/>
          <path d="m 807.0145,683.54404 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path84" style="display:inline" clip-path="none"/>
          <path d="m 777.0145,686.54404 h 30" stroke="#1a1a1a" id="path85" style="display:inline" clip-path="none"/>
          <path d="m 870.7645,683.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path86" style="display:inline" clip-path="none"/>
          <path d="m 840.7645,686.66904 h 30" stroke="#1a1a1a" id="path87" style="display:inline" clip-path="none"/>
          <path d="m 250.7645,873.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path88" style="display:inline" clip-path="none"/>
          <path d="m 220.7645,876.66904 h 30" stroke="#1a1a1a" id="path89" style="display:inline" clip-path="none"/>
          <path d="m 310.7645,873.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path90" style="display:inline" clip-path="none"/>
          <path d="m 280.7645,876.66904 h 30" stroke="#1a1a1a" id="path91" style="display:inline" clip-path="none"/>
          <path d="m 427.86604,874.05464 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path92" style="display:inline" clip-path="none"/>
          <path d="m 397.86604,877.05464 h 30" stroke="#1a1a1a" id="path93" style="display:inline" clip-path="none"/>
          <path d="m 490.7645,873.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path94" style="display:inline" clip-path="none"/>
          <path d="m 460.7645,876.66904 h 30" stroke="#1a1a1a" id="path95" style="display:inline" clip-path="none"/>
          <path d="m 680.7645,873.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path98" style="display:inline" clip-path="none"/>
          <path d="m 650.7645,876.66904 h 30" stroke="#1a1a1a" id="path99" style="display:inline" clip-path="none"/>
          <path d="m 810.7645,873.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path100" style="display:inline" clip-path="none"/>
          <path d="m 780.7645,876.66904 h 30" stroke="#1a1a1a" id="path101" style="display:inline" clip-path="none"/>
          <path d="m 870.7645,873.66904 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path102" style="display:inline" clip-path="none"/>
          <path d="m 840.7645,876.66904 h 30" stroke="#1a1a1a" id="path103" style="display:inline" clip-path="none"/>
          <path d="m 198.2645,756.16904 116.5,0.5" stroke="#1a1a1a" stroke-width="2.5" id="path126" style="display:inline" clip-path="none"/>
          <path d="m 501.7645,686.66904 v 71" stroke="#1a1a1a" stroke-width="2" id="path127" style="display:inline" clip-path="none"/>
          <path d="m 441.48944,805.53793 v 71" stroke="#1a1a1a" stroke-width="2" id="path127-8-1" style="display:inline" clip-path="none"/>
          <path d="m 381.94702,804.46596 v 71" stroke="#1a1a1a" stroke-width="2" id="path127-8-1-5" style="display:inline" clip-path="none"/>
          <path d="m 594.05756,686.86184 v 71" stroke="#1a1a1a" stroke-width="2" id="path128" style="display:inline" clip-path="none"/>
          <path d="m 530.13982,716.51736 v 41.50129" stroke="#1a1a1a" stroke-width="1.52908" id="path128-7" style="display:inline" clip-path="none"/>
          <path d="m 598.53424,797.7297 v 41.50129" stroke="#1a1a1a" stroke-width="1.52908" id="path128-7-6" style="display:inline" clip-path="none"/>
          <path d="M 530.90349,717.17051 H 500.77752" stroke="#1a1a1a" stroke-width="1.30278" id="path128-7-9" style="display:inline" clip-path="none"/>
          <path d="m 823.74393,756.47624 v 47" stroke="#1a1a1a" stroke-width="2.16795" id="path129" style="display:inline" clip-path="none"/>
          <path d="m 823.61893,772.10124 v 15" stroke="#fcfcfc" stroke-width="7" id="path130" style="display:inline" clip-path="none"/>
          <path d="m 197.1791,803.46287 245.3176,0.48608" stroke="#1a1a1a" stroke-width="3.57692" id="path126-9" style="display:inline" clip-path="none"/>
          <path d="m 404.13982,804.43382 h 15" stroke="#fcfcfc" stroke-width="7" id="path37-5-1" style="display:inline" clip-path="none"/>
          <path d="m 306.9513,804.839 h 58.42163" stroke="#fcfcfc" stroke-width="13.8146" id="path37-5-1-7" style="display:inline" clip-path="none"/>
          <path d="m 658.31053,804.31259 h 28.49683" stroke="#fcfcfc" stroke-width="9.6483" id="path43-2" style="display:inline" clip-path="none"/>
          <rect style="fill:#000000;fill-opacity:1;stroke-width:0.5" id="rect20" width="8.2904882" height="7.51928" x="480.88019" y="794.70508" clip-path="none"/>
          <rect style="fill:#000000;fill-opacity:1;stroke-width:0.5" id="rect20-8" width="8.2904882" height="7.51928" x="535.89044" y="794.70508" clip-path="none"/>
          <rect style="fill:#000000;fill-opacity:1;stroke-width:0.5" id="rect20-4" width="8.2904882" height="7.51928" x="591.28949" y="795.45508" clip-path="none"/>
          <path d="m 537.10765,756.69417 h 15" stroke="#fcfcfc" stroke-width="7" id="path43-8-8" style="display:inline" clip-path="none"/>
          <line x1="499.24933" y1="687.89001" x2="571.24933" y2="687.89001" stroke="#1a1a1a" stroke-width="2.5" id="line1-6" style="display:inline" clip-path="none"/>
          <path d="m 783.90834,756.90387 h 15" stroke="#fcfcfc" stroke-width="7" id="path44-3" style="display:inline" clip-path="none"/>
          <path d="m 826.7645,756.75483 h 15" stroke="#fcfcfc" stroke-width="7" id="path44-3-9" style="display:inline" clip-path="none"/>
          <path d="m 848.4664,756.99226 h 15" stroke="#fcfcfc" stroke-width="7" id="path44-3-3" style="display:inline" clip-path="none"/>
          <path d="m 874.00194,757.11358 h 15" stroke="#fcfcfc" stroke-width="7" id="path44-3-8" style="display:inline" clip-path="none"/>
          <path d="m 720.7645,803.66904 h 15" stroke="#fcfcfc" stroke-width="7" id="path44-3-2" style="display:inline" clip-path="none"/>
          <path d="m 703.0145,826.16904 v -15" stroke="#fcfcfc" stroke-width="7" id="path44-3-1" style="display:inline" clip-path="none"/>
          <rect style="fill:#000000;fill-opacity:1;stroke-width:1.18375" id="rect23" width="131.99902" height="2.1429999" x="765.8288" y="803.0257" clip-path="none"/>
          <path d="m 786.7645,804.16904 h 15" stroke="#fcfcfc" stroke-width="7" id="path44-3-0" style="display:inline" clip-path="none"/>
          <path d="m 598.28575,803.73555 h 42.37629" stroke="#1a1a1a" stroke-width="1.54512" id="path128-7-61" style="display:inline" clip-path="none"/>
          <rect style="fill-opacity:1;stroke:#1a1a1a;stroke-width:5;stroke-dasharray:none;stroke-opacity:1" id="rect32" width="150.3455" height="274.74551" x="895.7041" y="686.70984" clip-path="none"/>
          <rect style="fill-opacity:1;stroke:#1a1a1a;stroke-width:5;stroke-dasharray:none;stroke-opacity:1" id="rect32-4" width="150.3455" height="274.74551" x="45.177711" y="686.66907" clip-path="none"/>
          <path d="m 195.19381,763.19861 v 30.80976" stroke="#fcfcfc" stroke-width="10.0322" id="path38" style="display:inline" clip-path="none"/>
          <path d="m 895.788,764.53731 v 25.96016" stroke="#fcfcfc" stroke-width="9.20886" id="path130-8" style="display:inline" clip-path="none"/>

          <!-- Кабинеты и именованные помещения. -->
<rect x="197.08" y="688.31" width="160.31" height="69.41" rx="4" ry="4" class="room" v-bind="roomBind('112')"/>
          <rect x="502.05" y="688.05" width="91.77" height="68.33" rx="4" ry="4" class="room" v-bind="roomBind('rect-garderob')"/>
          <rect x="197.27" y="804.38" width="184.7" height="70.76" rx="4" ry="4" class="room" v-bind="roomBind('rect-canteen')"/>
          <rect x="358.53" y="687.84" width="62.17" height="68.85" rx="4" ry="4" class="room" v-bind="roomBind('rect-bufet')"/>
          <rect x="381.84" y="804.54" width="59.85" height="71.17" rx="4" ry="4" class="room" v-bind="roomBind('102')"/>
          <rect x="641.01" y="688.25" width="62.99" height="68.17" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-right')"/>
          <rect x="421.52" y="686.61" width="80.16" height="70.35" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-left')"/>
          <rect x="757.51" y="688.17" width="66.25" height="69.0" rx="4" ry="4" class="room" v-bind="roomBind('rect-medical')"/>
          <rect x="704.01" y="687.17" width="53.5" height="68.75" rx="4" ry="4" class="room" v-bind="roomBind('101')"/>
          <rect x="641.35" y="804.86" width="62.05" height="70.0" rx="4" ry="4" class="room" v-bind="roomBind('109')"/>
          <rect x="594.01" y="688.17" width="46.25" height="68.75" rx="4" ry="4" class="room" v-bind="roomBind('115')"/>
          <rect x="703.64" y="804.67" width="60.62" height="70.12" rx="4" ry="4" class="room" v-bind="roomBind('rect-reading')"/>
          <rect x="764.76" y="804.92" width="129.25" height="70.25" rx="4" ry="4" class="room" v-bind="roomBind('rect-library')"/>
          <rect x="895.68" y="687.67" width="150.5" height="274.5" rx="4" ry="4" class="room" v-bind="roomBind('rect-gym')"/>
          <rect x="44.68" y="686.17" width="150.5" height="274.5" rx="4" ry="4" class="room" v-bind="roomBind('rect-hall')"/>

          <!-- Подписи кабинетов (центрированы поверх прямоугольников). -->
<text x="277.24" y="731.65" class="room-label">112</text>
          <text x="547.94" y="727.25" class="room-label small">Гардероб</text>
          <text x="289.62" y="844.8" class="room-label small">Столовая</text>
          <text x="389.61" y="727.3" class="room-label small">Буфет</text>
          <text x="411.76" y="848.76" class="room-label">102</text>
          <text x="672.5" y="730.98" class="room-label">Л</text>
          <text x="461.6" y="730.42" class="room-label">Л</text>
          <text x="790.63" y="727.11" class="room-label small" font-size="12.33">Медпункт</text>
          <text x="730.76" y="730.18" class="room-label">101</text>
          <text x="672.38" y="848.5" class="room-label">109</text>
          <text x="617.13" y="730.02" class="room-label" font-size="20.76">115</text>
          <text x="733.95" y="838.11" class="room-label small" font-size="9.82">Читальный</text>
          <text x="733.95" y="848.42" class="room-label small" font-size="9.82">зал</text>
          <text x="829.38" y="845.08" class="room-label small">Библиотека</text>
          <text x="970.93" y="829.96" class="room-label small">Спортзал</text>
          <text x="119.93" y="828.46" class="room-label small">Актовый зал</text>
        </g>

        <!-- Точка инфо-стенда («вы здесь») — в координатах viewBox. -->
        <g class="stand-marker">
          <circle class="stand-halo" cx="539.35" cy="234.94" r="12"/>
          <circle class="stand-dot"  cx="539.35" cy="234.94" r="6"/>
        </g>
      </svg>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

// Маппинг room_type (из бэкенда) → CSS-класс цвета.
const TYPE_KEY_BY_LABEL = {
  'Аудитория': 'auditorium',
  'Лаборатория': 'lab',
  'Спортзал': 'sport',
  'Актовый зал': 'hall',
  'Приёмная': 'admin',
  'Приемная': 'admin',
}

// Карта именованных (не-числовых) кабинетов в типы — для подсветки и легенды.
const NAMED_TYPE_KEY = {
  'rect-reception': 'admin',
  'rect-wc-w': 'wc',
  'rect-wc-m': 'wc',
  'rect-stairs-left': 'stairs',
  'rect-stairs-center': 'stairs',
  'rect-stairs-right': 'stairs',
  'rect-hall': 'hall',
  'rect-gym': 'sport',
  'rect-library': 'library',
  'rect-reading': 'library',
  'rect-medical': 'medical',
  'rect-bufet': 'food',
  'rect-canteen': 'food',
  'rect-garderob': 'garderob',
}

export default {
  name: 'MapFloor1',
  props: {
    highlightFreeRooms: { type: Boolean, default: false },
    freeRooms: { type: Array, default: () => [] },
    busyRooms: { type: Array, default: () => [] },
    highlightedRoom: { type: String, default: null },
    // Мапа roomNumber → room_type из /rooms/floor/1.
    roomTypes: { type: Object, default: () => ({}) },
  },
  emits: ['room-click'],
  setup(props, { emit }) {
    const freeSet = computed(() => new Set(props.freeRooms.map((r) => String(r).trim())))
    const busySet = computed(() => new Set(props.busyRooms.map((r) => String(r).trim())))
    const target = computed(() => (props.highlightedRoom ? String(props.highlightedRoom).trim() : null))

    const roomBind = (label) => {
      const value = String(label).trim()
      const isNumeric = /^\d+$/.test(value)
      let typeKey
      if (isNumeric) {
        const typeLabel = props.roomTypes[value]
        typeKey = TYPE_KEY_BY_LABEL[typeLabel] || 'other'
      } else {
        typeKey = NAMED_TYPE_KEY[value] || 'other'
      }
      return {
        'data-room': isNumeric ? value : null,
        class: [
          `room--type-${typeKey}`,
          {
            'room--interactive': isNumeric,
            'room--free': props.highlightFreeRooms && freeSet.value.has(value),
            'room--busy': props.highlightFreeRooms && busySet.value.has(value),
            'room--target': target.value !== null && target.value === value,
          },
        ],
      }
    }

    const handleSvgClick = (event) => {
      const t = event.target
      if (!t || typeof t.getAttribute !== 'function') return
      const num = t.getAttribute('data-room')
      if (!num) return
      emit('room-click', num)
    }

    return {
      roomBind,
      handleSvgClick,
    }
  },
}
</script>

<style scoped>
.map-floor {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
}

.map-header {
  margin-bottom: 2rem;
  text-align: center;
}

.map-header h2 {
  color: var(--text);
  font-size: 2rem;
  margin-bottom: 1rem;
}

.map-container {
  background: var(--surface);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1px solid var(--border);
  border-radius: 25px;
  padding: 2rem;
  box-shadow: var(--shadow);
  overflow: auto;
}

.map-container svg {
  max-width: 100%;
  height: auto;
  display: block;
  margin: 0 auto;
}

text {
  pointer-events: none;
  user-select: none;
  fill: #000000 !important;
}

.room-label {
  font-size: 24px;
  font-weight: bold;
  fill: #000000 !important;
  text-anchor: middle;
  pointer-events: none;
}

.room-label.small {
  font-size: 14px;
  fill: #475569 !important;
  font-weight: 600;
}

.room {
  fill: transparent;
  stroke: transparent;
  cursor: default;
  transition: fill 0.25s ease, stroke 0.25s ease, fill-opacity 0.25s ease, stroke-opacity 0.25s ease;
  filter: url(#room-shadow-1);
}

.room.room--interactive {
  cursor: pointer;
}

.room--type-auditorium { fill: #3b82f6; fill-opacity: 0.22; stroke: #1d4ed8; stroke-opacity: 0.7;  stroke-width: 1.3; }
.room--type-lab        { fill: #8b5cf6; fill-opacity: 0.26; stroke: #6d28d9; stroke-opacity: 0.75; stroke-width: 1.3; }
.room--type-sport      { fill: #22c55e; fill-opacity: 0.26; stroke: #15803d; stroke-opacity: 0.75; stroke-width: 1.3; }
.room--type-hall       { fill: #f97316; fill-opacity: 0.26; stroke: #c2410c; stroke-opacity: 0.75; stroke-width: 1.3; }
.room--type-admin      { fill: #f59e0b; fill-opacity: 0.30; stroke: #b45309; stroke-opacity: 0.8;  stroke-width: 1.3; }
/* Туалеты — отчётливый тёплый розовый, чтобы не сливаться с пустым (--other) и не путаться с лестницей. */
.room--type-wc         { fill: #ec4899; fill-opacity: 0.22; stroke: #be185d; stroke-opacity: 0.7;  stroke-width: 1.3; }
.room--type-stairs     { fill: #6366f1; fill-opacity: 0.26; stroke: #4338ca; stroke-opacity: 0.75; stroke-width: 1.3; stroke-dasharray: 6 4; }
/* Библиотека и читальный зал — бирюзовый. */
.room--type-library    { fill: #14b8a6; fill-opacity: 0.24; stroke: #0f766e; stroke-opacity: 0.75; stroke-width: 1.3; }
/* Медпункт — ярко-красный, чтобы было заметно в экстренном случае. */
.room--type-medical    { fill: #ef4444; fill-opacity: 0.22; stroke: #b91c1c; stroke-opacity: 0.8;  stroke-width: 1.3; }
/* Буфет и столовая — тёплый жёлтый. */
.room--type-food       { fill: #eab308; fill-opacity: 0.30; stroke: #a16207; stroke-opacity: 0.8;  stroke-width: 1.3; }
/* Гардероб — нейтральный сине-серый. */
.room--type-garderob   { fill: #64748b; fill-opacity: 0.20; stroke: #334155; stroke-opacity: 0.7;  stroke-width: 1.3; }
/* Кабинеты без известного типа — почти прозрачные, чтобы не конкурировать с цветными типами и не выглядеть «использованной» подсветкой. */
.room--type-other      { fill: #cbd5e1; fill-opacity: 0.10; stroke: #94a3b8; stroke-opacity: 0.55; stroke-width: 1; }

/* «Вы здесь» — маркер инфо-стенда. */
.stand-marker {
  pointer-events: none;
}

.stand-marker .stand-halo {
  fill: rgba(37, 99, 235, 0.25);
  animation: stand-halo-pulse-1 1.8s ease-in-out infinite;
}

.stand-marker .stand-dot {
  fill: #2563eb;
  stroke: #ffffff;
  stroke-width: 2;
}

@keyframes stand-halo-pulse-1 {
  0%, 100% { opacity: 0.55; transform: scale(1); }
  50%      { opacity: 0.15; transform: scale(1.6); }
}

.stand-marker .stand-halo {
  transform-origin: center;
  transform-box: fill-box;
}

.room.room--interactive:hover {
  fill-opacity: 0.25;
  stroke-opacity: 1;
  stroke-width: 2;
}

.room.room--target {
  fill: rgba(37, 99, 235, 0.35) !important;
  stroke: #2563eb !important;
  stroke-width: 3 !important;
  animation: room-target-pulse-1 1.6s ease-in-out infinite;
}

@keyframes room-target-pulse-1 {
  0%, 100% {
    fill: rgba(37, 99, 235, 0.35) !important;
    stroke-opacity: 1;
  }
  50% {
    fill: rgba(37, 99, 235, 0.55) !important;
    stroke-opacity: 0.6;
  }
}

.room.room--free {
  fill: rgba(34, 197, 94, 0.32) !important;
  stroke: rgba(22, 163, 74, 0.85) !important;
  stroke-width: 2 !important;
  animation: room-free-pulse-1 2.4s ease-in-out infinite;
}

.room.room--busy {
  fill: rgba(239, 68, 68, 0.18) !important;
  stroke: rgba(220, 38, 38, 0.6) !important;
  stroke-width: 1.5 !important;
}

@keyframes room-free-pulse-1 {
  0%, 100% { fill: rgba(34, 197, 94, 0.28) !important; }
  50%      { fill: rgba(34, 197, 94, 0.42) !important; }
}
</style>
