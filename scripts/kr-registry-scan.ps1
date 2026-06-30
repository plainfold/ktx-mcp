$terms = @(
  # 교통 (v7에서 일부)
  'korail','ktx','srt','kobus','express-bus','intercity','hipass','toll','parking','taxi','kakao-t','uber','bike','ddareungi','ferry','jeju-ferry','airport','incheon','gimpo','gimhae',
  # 지도·로컬
  'kakao','naver','tmap','odsay','transit','subway','bus','seoul-metro',
  # 공공·행정
  'data-go-kr','opendata','public-data','unipass','customs','hometax','nts','gov24','minwon','immigration','visa','arc','alien','passport',
  # 금융·경제
  'ecos','bok','krw','exchange','stock','krx','kospi','dart','pykrx','toss','kakaopay','bank','loan','jeonse','real-estate','apartment','molit',
  # 생활·소비
  'baemin','yogiyo','coupang','delivery','gmarket','11st','musinsa','daangn','bunjang','melon','lotto','concert','ticket','interpark',
  # 의료·복지
  'hospital','pharmacy','hira','nhis','vaccine','emergency','119','welfare','childcare','pension',
  # 관광·문화
  'tourism','visit-seoul','kto','festival','museum','hanok',
  # 날씨·환경
  'weather','air-quality','pm25','dust','kma',
  # 법률·규제 (제외 후보지만 스캔)
  'korean-law','taxlaw','labor-law','ai-basic-act',
  # 교육·취업
  'university','csat','suneung','jobkorea','saramin','worknet',
  # 농수산·에너지
  'agriculture','fishery','ev-charger','kepco','gas-station',
  # 통신
  'sim-card','esim','skt','kt-telecom','lg-uplus',
  # 지역
  'seoul','busan','jeju','gyeonggi','incheon-city',
  # 한국 일반
  'korea','korean','south-korea','hangul','hwp'
)
$base = 'https://registry.modelcontextprotocol.io/v0.1/servers?search={0}&version=latest'
$results = foreach ($t in $terms) {
  try {
    $r = Invoke-RestMethod -Uri ($base -f [uri]::EscapeDataString($t)) -TimeoutSec 12
    $n = if ($r.servers) { $r.servers.Count } else { 0 }
    [pscustomobject]@{ term = $t; count = $n }
  } catch {
    [pscustomobject]@{ term = $t; count = -1 }
  }
  Start-Sleep -Milliseconds 200
}
$results | Sort-Object count, term | Format-Table -AutoSize
Write-Host "--- nonzero ---"
$results | Where-Object { $_.count -gt 0 } | Sort-Object -Descending count | Format-Table -AutoSize
