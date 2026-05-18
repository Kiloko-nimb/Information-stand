<template>
  <div class="map-floor">
    <div class="map-header">
      <h2>2 этаж</h2>
    </div>

    <div class="map-container">
      <svg
        width="820"
        height="900"
        viewBox="0 0 820 900"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        @click="handleSvgClick"
      >
        <defs>
          <!-- Точечный фон коридоров — снимает белизну чертёжной заливки. -->
          <pattern id="bg-dots-2" x="0" y="0" width="22" height="22" patternUnits="userSpaceOnUse">
            <rect width="22" height="22" fill="#f8fafc"/>
            <circle cx="11" cy="11" r="1" fill="#cbd5e1" opacity="0.65"/>
          </pattern>
          <!-- Лёгкая тень под комнатами для объёма. -->
          <filter id="room-shadow-2" x="-10%" y="-10%" width="120%" height="120%">
            <feDropShadow dx="0" dy="2" stdDeviation="2" flood-color="#0f172a" flood-opacity="0.08"/>
          </filter>
        </defs>

        <rect x="0" y="0" width="820" height="900" fill="url(#bg-dots-2)"/>

        <g>
          <!-- Стены, двери и прочая графика из исходного Inkscape-файла. -->
<line x1="365" y1="538.75" x2="437" y2="538.75" stroke="#1a1a1a" stroke-width="2.5" id="line1" style="display:inline"/>
          <path d="M 220,140 H 365 V 90 h 70 v 50 H 580 V 540 H 435 V 640 H 760 V 830 H 60 V 640 H 365 V 540 H 220 Z" stroke="#1a1a1a" stroke-width="5" stroke-linecap="square" id="path1" style="display:inline"/>
          <path d="M 365,140 V 540" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path2" style="display:inline"/>
          <path d="M 435,140 V 540" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path3" style="display:inline"/>
          <path d="M 220,250 H 365" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path4" style="display:inline"/>
          <path d="M 220,360 H 365" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path5" style="display:inline"/>
          <path d="M 220,440 H 365" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path6" style="display:inline"/>
          <path d="M 435,250 H 580" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path7" style="display:inline"/>
          <path d="M 435,360 H 580" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path8" style="display:inline"/>
          <path d="M 435,440 H 580" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path9" style="display:inline"/>
          <path d="m 320,540 v -40 h 45" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path10" style="display:inline"/>
          <path d="M 180,710 H 365" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path11" style="display:inline"/>
          <path d="M 435,710 H 620" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path12" style="display:inline"/>
          <path d="M 60,750 H 760" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path13" style="display:inline"/>
          <path d="m 220,640 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path14" style="display:inline"/>
          <path d="m 300,640 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path15" style="display:inline"/>
          <path d="m 162,710 v 40" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path16" style="display:inline"/>
          <path d="m 205,750 v 80" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path17" style="display:inline"/>
          <path d="m 285,750 v 80" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path18" style="display:inline"/>
          <path d="m 395,750 v 80" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path19" style="display:inline"/>
          <path d="m 435,750 v 80" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path20" style="display:inline"/>
          <path d="m 505,640 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path21" style="display:inline"/>
          <path d="m 568,639 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path22" style="display:inline"/>
          <path d="M 620,710 H 760" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path23" style="display:inline"/>
          <path d="m 500,750 v 80" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path24" style="display:inline"/>
          <path d="m 564.5,750 v 80" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path25" style="display:inline"/>
          <path d="M 597,709.5 620,685 v -43.5" stroke="#1a1a1a" stroke-width="1.5" id="path26" style="display:inline"/>
          <path d="M 605.5,750.5 620,773 v 57" stroke="#1a1a1a" stroke-width="1.5" id="path27" style="display:inline"/>
          <path d="m 410,665 h -20 v 10 h 20 z" stroke="#1a1a1a" stroke-width="1.5" id="path28" style="display:inline"/>
          <path d="m 365,220 v 20" stroke="#fcfcfc" stroke-width="7" id="path29" style="display:inline"/>
          <path d="m 365,260 v 20" stroke="#fcfcfc" stroke-width="7" id="path30" style="display:inline"/>
          <path d="m 365,410 v 20" stroke="#fcfcfc" stroke-width="7" id="path31" style="display:inline"/>
          <path d="m 365,450 v 20" stroke="#fcfcfc" stroke-width="7" id="path32" style="display:inline"/>
          <path d="m 435,220 v 20" stroke="#fcfcfc" stroke-width="7" id="path33" style="display:inline"/>
          <path d="m 435,260 v 20" stroke="#fcfcfc" stroke-width="7" id="path34" style="display:inline"/>
          <path d="m 435,410 v 20" stroke="#fcfcfc" stroke-width="7" id="path35" style="display:inline"/>
          <path d="m 435,450 v 20" stroke="#fcfcfc" stroke-width="7" id="path36" style="display:inline"/>
          <path d="m 309,710 h 15" stroke="#fcfcfc" stroke-width="7" id="path37" style="display:inline"/>
          <path d="m 162,720 v 15" stroke="#fcfcfc" stroke-width="7" id="path38" style="display:inline"/>
          <path d="m 185,750 h 15" stroke="#fcfcfc" stroke-width="7" id="path39" style="display:inline"/>
          <path d="m 235,750 h 15" stroke="#fcfcfc" stroke-width="7" id="path40" style="display:inline"/>
          <path d="m 330,750 h 15" stroke="#fcfcfc" stroke-width="7" id="path41" style="display:inline"/>
          <path d="m 405,750 h 15" stroke="#fcfcfc" stroke-width="7" id="path42" style="display:inline"/>
          <path d="m 460,710 h 15" stroke="#fcfcfc" stroke-width="7" id="path43" style="display:inline"/>
          <path d="m 630,710 h 15" stroke="#fcfcfc" stroke-width="7" id="path44" style="display:inline"/>
          <path d="M 605,701.066 615.127,690" stroke="#fcfcfc" stroke-width="7" id="path45" style="display:inline"/>
          <path d="m 445,750 h 15" stroke="#fcfcfc" stroke-width="7" id="path46" style="display:inline"/>
          <path d="m 520,750 h 15" stroke="#fcfcfc" stroke-width="7" id="path47" style="display:inline"/>
          <path d="m 630,750 h 15" stroke="#fcfcfc" stroke-width="7" id="path48" style="display:inline"/>
          <path d="m 184.5,709 h 15" stroke="#fcfcfc" stroke-width="7" id="path49" style="display:inline"/>
          <path d="M 410,539 H 390" stroke="#fcfcfc" stroke-width="9" id="path50" style="display:inline"/>
          <path d="m 365,95 h 70 m -70,6 h 70 m -70,6 h 70 m -70,6 h 70 m -70,6 h 70 m -70,6 h 70 m -70,6 h 70" stroke="#1a1a1a" stroke-width="1.5" id="path51" style="display:inline"/>
          <path d="m 260,640 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path52" style="display:inline"/>
          <path d="m 220,645 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40" stroke="#1a1a1a" stroke-width="1.5" id="path53" style="display:inline"/>
          <path d="m 260,645 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40 m -40,6 h 40" stroke="#1a1a1a" stroke-width="1.5" id="path54" style="display:inline"/>
          <path d="m 536.5,640 v 70" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path55" style="display:inline"/>
          <path d="m 506,645 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30" stroke="#1a1a1a" stroke-width="1.5" id="path56" style="display:inline"/>
          <path d="m 537,645 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30 m -30,6 h 30" stroke="#1a1a1a" stroke-width="1.5" id="path57" style="display:inline"/>
          <path d="m 223,180 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path58" style="display:inline"/>
          <path d="m 220,180 v 30" stroke="#1a1a1a" id="path59" style="display:inline"/>
          <path d="m 223,290 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path60" style="display:inline"/>
          <path d="m 220,290 v 30" stroke="#1a1a1a" id="path61" style="display:inline"/>
          <path d="m 223,385 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path62" style="display:inline"/>
          <path d="m 220,385 v 30" stroke="#1a1a1a" id="path63" style="display:inline"/>
          <path d="m 223,475 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path64" style="display:inline"/>
          <path d="m 220,475 v 30" stroke="#1a1a1a" id="path65" style="display:inline"/>
          <path d="m 60,660 v 30" stroke="#1a1a1a" id="path66" style="display:inline"/>
          <path d="m 60,715 v 30" stroke="#1a1a1a" id="path67" style="display:inline"/>
          <path d="m 583,180 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path68" style="display:inline"/>
          <path d="m 580,180 v 30" stroke="#1a1a1a" id="path69" style="display:inline"/>
          <path d="m 583,290 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path70" style="display:inline"/>
          <path d="m 580,290 v 30" stroke="#1a1a1a" id="path71" style="display:inline"/>
          <path d="m 583,385 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path72" style="display:inline"/>
          <path d="m 580,385 v 30" stroke="#1a1a1a" id="path73" style="display:inline"/>
          <path d="m 583,475 h -6 v 30 h 6 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path74" style="display:inline"/>
          <path d="m 580,475 v 30" stroke="#1a1a1a" id="path75" style="display:inline"/>
          <path d="m 760,660 v 30" stroke="#1a1a1a" id="path76" style="display:inline"/>
          <path d="m 760,775 v 30" stroke="#1a1a1a" id="path77" style="display:inline"/>
          <path d="m 135,637 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path78" style="display:inline"/>
          <path d="m 105,640 h 30" stroke="#1a1a1a" id="path79" style="display:inline"/>
          <path d="m 215,637 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path80" style="display:inline"/>
          <path d="m 185,640 h 30" stroke="#1a1a1a" id="path81" style="display:inline"/>
          <path d="m 482,637 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path82" style="display:inline"/>
          <path d="m 452,640 h 30" stroke="#1a1a1a" id="path83" style="display:inline"/>
          <path d="m 675,637 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path84" style="display:inline"/>
          <path d="m 645,640 h 30" stroke="#1a1a1a" id="path85" style="display:inline"/>
          <path d="m 735,637 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path86" style="display:inline"/>
          <path d="m 705,640 h 30" stroke="#1a1a1a" id="path87" style="display:inline"/>
          <path d="M 115,827 H 85 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path88" style="display:inline"/>
          <path d="m 85,830 h 30" stroke="#1a1a1a" id="path89" style="display:inline"/>
          <path d="m 175,827 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path90" style="display:inline"/>
          <path d="m 145,830 h 30" stroke="#1a1a1a" id="path91" style="display:inline"/>
          <path d="m 260,827 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path92" style="display:inline"/>
          <path d="m 230,830 h 30" stroke="#1a1a1a" id="path93" style="display:inline"/>
          <path d="m 355,827 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path94" style="display:inline"/>
          <path d="m 325,830 h 30" stroke="#1a1a1a" id="path95" style="display:inline"/>
          <path d="m 482,827 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path96" style="display:inline"/>
          <path d="m 452,830 h 30" stroke="#1a1a1a" id="path97" style="display:inline"/>
          <path d="m 545,827 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path98" style="display:inline"/>
          <path d="m 515,830 h 30" stroke="#1a1a1a" id="path99" style="display:inline"/>
          <path d="m 675,827 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path100" style="display:inline"/>
          <path d="m 645,830 h 30" stroke="#1a1a1a" id="path101" style="display:inline"/>
          <path d="m 735,827 h -30 v 6 h 30 z" fill="#fcfcfc" stroke="#1a1a1a" stroke-width="1.5" id="path102" style="display:inline"/>
          <path d="m 705,830 h 30" stroke="#1a1a1a" id="path103" style="display:inline"/>
          <path d="M 62.5,709.5 179,710" stroke="#1a1a1a" stroke-width="2.5" id="path126" style="display:inline"/>
          <path d="m 366,640 v 71" stroke="#1a1a1a" stroke-width="2" id="path127" style="display:inline"/>
          <path d="m 434,640 v 71" stroke="#1a1a1a" stroke-width="2" id="path128" style="display:inline"/>
          <path d="m 666,710 v 40" stroke="#1a1a1a" stroke-width="2" id="path129" style="display:inline"/>
          <path d="m 666,722 v 15" stroke="#fcfcfc" stroke-width="7" id="path130" style="display:inline"/>
          <path d="m 577.5,641.5 v 69 m -1.5,39 V 828" stroke="#1a1a1a" stroke-width="2.5" id="path131" style="display:inline"/>
          <path d="m 400.5,93 v 37.5" stroke="#1a1a1a" stroke-width="2.5" stroke-linecap="square" id="path132" style="display:inline"/>
          <path d="m 609,756 8.188,12.568" stroke="#fcfcfc" stroke-width="7" id="path133" style="display:inline"/>
          <path d="M 220,173.75 H 364" stroke="#1a1a1a" stroke-width="2.5" id="path134" style="display:inline"/>

          <!-- Кабинеты и именованные помещения. -->
<rect x="220.95" y="249.87" width="144.6" height="111.05" rx="4" ry="4" class="room" v-bind="roomBind('213')"/>
          <rect x="220.95" y="360.93" width="143.83" height="79.05" rx="4" ry="4" class="room" v-bind="roomBind('212')"/>
          <rect x="434.58" y="249.87" width="143.83" height="109.9" rx="4" ry="4" class="room" v-bind="roomBind('216')"/>
          <rect x="435.35" y="360.93" width="144.22" height="79.05" rx="4" ry="4" class="room" v-bind="roomBind('217')"/>
          <rect x="434.96" y="441.13" width="143.06" height="97.17" rx="4" ry="4" class="room" v-bind="roomBind('218')"/>
          <rect x="221.34" y="440.36" width="143.06" height="98.33" rx="4" ry="4" class="room" v-bind="roomBind('211')"/>
          <rect x="666.32" y="709.51" width="92.16" height="40.1" rx="4" ry="4" class="room" v-bind="roomBind('202')"/>
          <rect x="433.8" y="640.87" width="71.34" height="68.25" rx="4" ry="4" class="room" v-bind="roomBind('219')"/>
          <rect x="285.35" y="750.39" width="109.9" height="77.89" rx="4" ry="4" class="room" v-bind="roomBind('207')"/>
          <rect x="434.58" y="750.39" width="65.55" height="78.66" rx="4" ry="4" class="room" v-bind="roomBind('205')"/>
          <rect x="499.74" y="750.77" width="64.4" height="78.28" rx="4" ry="4" class="room" v-bind="roomBind('204')"/>
          <rect x="578.02" y="641.65" width="179.69" height="67.87" rx="4" ry="4" class="room" v-bind="roomBind('201')"/>
          <rect x="576.48" y="750.39" width="181.23" height="77.89" rx="4" ry="4" class="room" v-bind="roomBind('203')"/>
          <rect x="205.14" y="750.39" width="79.82" height="77.31" rx="4" ry="4" class="room" v-bind="roomBind('208')"/>
          <rect x="61.31" y="750.19" width="143.06" height="78.08" rx="4" ry="4" class="room" v-bind="roomBind('210')"/>
          <rect x="61.35" y="641.85" width="157.6" height="67.62" rx="4" ry="4" class="room" v-bind="roomBind('209')"/>
          <rect x="299.66" y="641.03" width="65.71" height="68.17" rx="4" ry="4" class="room" v-bind="roomBind('rect-wc-w')"/>
          <rect x="365.36" y="89.85" width="67.87" height="41.45" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-center')"/>
          <rect x="220.18" y="640.1" width="80.01" height="70.18" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-left')"/>
          <rect x="504.56" y="641.26" width="63.05" height="68.44" rx="4" ry="4" class="room" v-bind="roomBind('rect-stairs-right')"/>
          <rect x="394.82" y="750.1" width="40.35" height="79.35" rx="4" ry="4" class="room" v-bind="roomBind('rect-reception')"/>
          <rect x="220.86" y="141.51" width="144.51" height="107.7" rx="4" ry="4" class="room" v-bind="roomBind('214')"/>
          <rect x="435.17" y="141.24" width="143.15" height="107.97" rx="4" ry="4" class="room" v-bind="roomBind('215')"/>

          <!-- Подписи кабинетов (центрированы поверх прямоугольников). -->
<text x="293.25" y="314.03" class="room-label">213</text>
          <text x="292.87" y="409.09" class="room-label">212</text>
          <text x="506.5" y="313.46" class="room-label">216</text>
          <text x="507.46" y="409.09" class="room-label">217</text>
          <text x="506.49" y="498.35" class="room-label">218</text>
          <text x="292.87" y="498.17" class="room-label">211</text>
          <text x="712.4" y="738.2" class="room-label">202</text>
          <text x="469.47" y="683.63" class="room-label">219</text>
          <text x="340.3" y="797.98" class="room-label">207</text>
          <text x="467.35" y="798.36" class="room-label">205</text>
          <text x="531.94" y="798.55" class="room-label">204</text>
          <text x="667.87" y="684.23" class="room-label">201</text>
          <text x="667.1" y="797.98" class="room-label">203</text>
          <text x="245.05" y="797.68" class="room-label">208</text>
          <text x="132.84" y="797.87" class="room-label">210</text>
          <text x="140.15" y="684.3" class="room-label">209</text>
          <text x="332.52" y="683.75" class="room-label">Ж</text>
          <text x="399.3" y="119.21" class="room-label">Л</text>
          <text x="260.19" y="683.83" class="room-label">Л</text>
          <text x="536.09" y="684.12" class="room-label">Л</text>
          <text x="415.0" y="793.01" class="room-label small" font-size="9">Приёмная</text>
          <text x="293.12" y="204.0" class="room-label">214</text>
          <text x="506.75" y="203.87" class="room-label">215</text>
        </g>

        <!-- Точка инфо-стенда («вы здесь») — в координатах viewBox. -->

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
  name: 'MapFloor2',
  props: {
    highlightFreeRooms: { type: Boolean, default: false },
    freeRooms: { type: Array, default: () => [] },
    busyRooms: { type: Array, default: () => [] },
    highlightedRoom: { type: String, default: null },
    // Мапа roomNumber → room_type из /rooms/floor/2.
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
  filter: url(#room-shadow-2);
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
  animation: stand-halo-pulse-2 1.8s ease-in-out infinite;
}

.stand-marker .stand-dot {
  fill: #2563eb;
  stroke: #ffffff;
  stroke-width: 2;
}

@keyframes stand-halo-pulse-2 {
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
  animation: room-target-pulse-2 1.6s ease-in-out infinite;
}

@keyframes room-target-pulse-2 {
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
  animation: room-free-pulse-2 2.4s ease-in-out infinite;
}

.room.room--busy {
  fill: rgba(239, 68, 68, 0.18) !important;
  stroke: rgba(220, 38, 38, 0.6) !important;
  stroke-width: 1.5 !important;
}

@keyframes room-free-pulse-2 {
  0%, 100% { fill: rgba(34, 197, 94, 0.28) !important; }
  50%      { fill: rgba(34, 197, 94, 0.42) !important; }
}
</style>
