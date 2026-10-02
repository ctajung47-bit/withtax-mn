  function earnedDed(g){let d;if(g<=5e6)d=g*.7;else if(g<=15e6)d=3.5e6+(g-5e6)*.4;else if(g<=45e6)d=7.5e6+(g-15e6)*.15;else if(g<=1e8)d=12e6+(g-45e6)*.05;else d=14.75e6+(g-1e8)*.02;return Math.min(d,2e7);}
  function calcTax(base,y){const br=y>=2023?[[14e6,.06],[50e6,.15],[88e6,.24],[150e6,.35],[300e6,.38],[500e6,.40],[1e9,.42],[Infinity,.45]]:[[12e6,.06],[46e6,.15],[88e6,.24],[150e6,.35],[300e6,.38],[500e6,.40],[1e9,.42],[Infinity,.45]];let t=0,prev=0;for(const [lim,r] of br){if(base>prev){t+=(Math.min(base,lim)-prev)*r;prev=lim;}else break;}return Math.max(0,t);}
  function earnedCredit(tax,g){let c=tax<=1.3e6?tax*.55:715000+(tax-1.3e6)*.3;let cap=g<=33e6?740000:g<=70e6?Math.max(660000,740000-(g-33e6)*.008):Math.max(500000,660000-(g-70e6)*.005);return Math.min(c,cap);}
  function yearTax(g,y,extraDed,relief){ // relief: ratio of income eligible 0..1
    if(g<=0)return {tax:0,calc:0,relief:0};
    const inc=g-earnedDed(g); const base=Math.max(0,inc-1.5e6-extraDed); const calcT=calcTax(base,y);
    const cap=y>=2023?2e6:1.5e6; const rel=relief>0?Math.min(calcT*relief*.9,cap):0;
    const credit=earnedCredit(calcT,g)*(calcT>0?(1-rel/calcT):1);
    const tax=Math.max(0,calcT-rel-credit-130000);
    return {tax,calc:calcT,relief:rel};
  }
