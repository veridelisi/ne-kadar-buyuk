import math
import streamlit as st


st.set_page_config(
    page_title="Ne Kadar Büyük?",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
)


VALUES = {
    "1 milyar TL": 1_000_000_000,
    "2 milyar TL": 2_000_000_000,
    "20 milyar TL": 20_000_000_000,
}

BENCHMARKS = [
    {
        "icon": "🏠",
        "title": "Ortalama konut",
        "unit": 5_311_000,
        "unit_label": "5.311.000 TL / konut",
        "source": "Endeksa – Türkiye ortalaması, Ağustos 2026",
        "url": "https://www.ekoturk.com/haberler/turkiyede-ortalama-konut-fiyati-53-milyon-tlyi-asti/",
        "kind": "count",
    },
    {
        "icon": "🚗",
        "title": "Fiat Egea Sedan",
        "unit": 1_499_900,
        "unit_label": "1.499.900 TL / otomobil",
        "source": "Ekim 2026 liste fiyatı",
        "url": "https://www.webtekno.com/ekim-2026-fiat-fiyat-listesi-h226429.html",
        "kind": "count",
    },
    {
        "icon": "👷",
        "title": "Bir yıllık net asgari ücret",
        "unit": 28_075.50 * 12,
        "unit_label": "28.075,50 TL × 12 ay",
        "source": "Çalışma ve Sosyal Güvenlik Bakanlığı – 2026",
        "url": "https://csgb.gov.tr/tr/poco-pages/asgari-ucret/",
        "kind": "people",
    },
    {
        "icon": "👴",
        "title": "Bir yıllık en düşük emekli aylığı",
        "unit": 23_552 * 12,
        "unit_label": "23.552 TL × 12 ay",
        "source": "Temmuz 2026 itibarıyla en düşük emekli aylığı",
        "url": "https://www.tbmm.gov.tr/Haber/Detay?Id=e52a308b-266d-4398-954b-019f279e7395",
        "kind": "people",
    },
    {
        "icon": "🏫",
        "title": "24 derslikli okul",
        "unit": 112_400_000,
        "unit_label": "112.400.000 TL / okul",
        "source": "2026 tarihli örnek yapım sözleşmesi",
        "url": "https://ihale.diyosis.com/ihale/2026-1224355-artuklu-24-derslikli-ortaokul-yapim-isi-1-kisim-kiziltepe-harabilme",
        "kind": "count",
    },
    {
        "icon": "🏥",
        "title": "150 yataklı devlet hastanesi",
        "unit": 1_544_700_000,
        "unit_label": "1.544.700.000 TL / hastane",
        "source": "Van Erciş 2026 yapım sözleşmesi",
        "url": "https://www.ihaledetay.com/2026-549141",
        "kind": "hospital",
    },
    {
        "icon": "🎓",
        "title": "Öğrenciye bir yıllık burs",
        "unit": 4_000 * 12,
        "unit_label": "4.000 TL × 12 ay",
        "source": "VGM yükseköğrenim bursu – 2026/27",
        "url": "https://ihale.vgm.gov.tr/sayfalar/burs-basvurulari",
        "kind": "students",
    },
    {
        "icon": "🍞",
        "title": "200 gram ekmek",
        "unit": 17.50,
        "unit_label": "17,50 TL / adet",
        "source": "2026 azami fiyat tarifesi",
        "url": "https://atonet.org.tr/Uploads/Birimler/Internet/Hizmetlerimiz/Azami%20Fiyat%20Tarifleri/2026_azami_fiyat_tarifesi/2026_ekmek_azami_fiyat_tarifesi_20260331.pdf",
        "kind": "count",
    },
]


def tr_number(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def result_text(amount: int, item: dict) -> tuple[str, str]:
    exact = amount / item["unit"]
    whole = math.floor(exact)

    if item["kind"] == "people":
        return tr_number(whole), "kişinin 1 yıllık geliri"
    if item["kind"] == "students":
        return tr_number(whole), "öğrenciye 1 yıllık burs"
    if item["kind"] == "hospital":
        remainder = amount - whole * item["unit"]
        if whole == 0:
            return f"%{exact * 100:.0f}", "bir hastanenin yapım maliyeti"
        return tr_number(whole), f"tam hastane · {tr_number(round(remainder / 1_000_000))} milyon TL kalır"
    return tr_number(whole), "adet"


st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(180deg, #f7f8fc 0%, #ffffff 38%);}
    .block-container {max-width: 1120px; padding-top: 2.2rem; padding-bottom: 3rem;}
    .hero {text-align:center; padding: 1.25rem 0 .6rem;}
    .hero-kicker {color:#b43b2f; font-weight:800; letter-spacing:.12em; font-size:.78rem;}
    .hero h1 {font-size:clamp(2.2rem, 6vw, 4.4rem); margin:.15rem 0; color:#152238; letter-spacing:-.04em;}
    .hero p {font-size:1.06rem; color:#5d6778; max-width:720px; margin:.4rem auto 1rem; line-height:1.65;}
    div[role="radiogroup"] {justify-content:center; gap:.6rem;}
    div[role="radiogroup"] label {background:#fff; border:1px solid #dfe4ec; padding:.65rem 1rem; border-radius:999px; box-shadow:0 4px 14px rgba(25,35,55,.05);}
    .amount-panel {margin:1.25rem 0 1.6rem; padding:1.25rem; border-radius:24px; background:#152238; color:white; text-align:center; box-shadow:0 14px 35px rgba(21,34,56,.18);}
    .amount-panel .eyebrow {font-size:.8rem; opacity:.72; letter-spacing:.08em; text-transform:uppercase;}
    .amount-panel .amount {font-size:clamp(2rem, 6vw, 3.8rem); font-weight:900; letter-spacing:-.04em; line-height:1.08;}
    .section-title {font-size:1.45rem; font-weight:850; color:#152238; margin:1.1rem 0 .75rem;}
    .card {height:100%; min-height:245px; background:#fff; border:1px solid #e6e9ef; border-radius:22px; padding:1.35rem; box-shadow:0 8px 24px rgba(31,45,70,.07); display:flex; flex-direction:column;}
    .card-icon {font-size:2rem;}
    .card-title {font-size:1rem; color:#596477; margin-top:.6rem; min-height:2.7rem;}
    .card-number {font-size:clamp(1.8rem, 4vw, 2.65rem); line-height:1.1; font-weight:900; color:#b43b2f; letter-spacing:-.03em; margin:.25rem 0;}
    .card-unit {font-size:.93rem; color:#152238; font-weight:700; min-height:2.5rem;}
    .card-source {font-size:.76rem; color:#7b8493; border-top:1px solid #edf0f4; padding-top:.7rem; margin-top:auto; line-height:1.45;}
    .card-source a {color:#526f9e; text-decoration:none;}
    .note {background:#fff7e8; border-left:5px solid #e4a73b; padding:1rem 1.1rem; border-radius:10px; color:#5d4a28; margin-top:1.5rem; line-height:1.55;}
    footer {visibility:hidden;}
    @media (max-width: 640px) {
        .block-container {padding:1rem .85rem 2rem;}
        .hero {padding-top:.4rem;}
        .card {min-height:220px;}
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
      <div class="hero-kicker">BÜYÜK PARAYI ANLAMA REHBERİ</div>
      <h1>Bu para ne kadar büyük?</h1>
      <p>Haberlerde geçen milyarlar gündelik hayatta neye karşılık geliyor? Bir tutar seçin; konut, otomobil, ücret ve kamu yatırımı karşılığını görün.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

selected = st.radio(
    "Karşılaştırılacak tutarı seçin",
    options=list(VALUES.keys()),
    index=1,
    horizontal=True,
    label_visibility="collapsed",
)
amount = VALUES[selected]

st.markdown(
    f"""
    <div class="amount-panel">
      <div class="eyebrow">Seçilen tutar</div>
      <div class="amount">{selected}</div>
    </div>
    <div class="section-title">Bu parayla yaklaşık olarak…</div>
    """,
    unsafe_allow_html=True,
)

for start in range(0, len(BENCHMARKS), 4):
    cols = st.columns(4)
    for col, item in zip(cols, BENCHMARKS[start : start + 4]):
        number, unit = result_text(amount, item)
        with col:
            st.markdown(
                f"""
                <div class="card">
                  <div class="card-icon">{item['icon']}</div>
                  <div class="card-title">{item['title']}</div>
                  <div class="card-number">{number}</div>
                  <div class="card-unit">{unit}</div>
                  <div class="card-source">
                    {item['unit_label']}<br>
                    <a href="{item['url']}" target="_blank">{item['source']} ↗</a>
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown(
    """
    <div class="note">
      <strong>Nasıl okumalı?</strong> Her kart alternatif bir karşılaştırmadır; ürünler birlikte alınmıyor. Sonuçlar belirtilen 2026 fiyatları üzerinden yaklaşık olarak hesaplanmış, satın alınabilecek tam adetler aşağı yuvarlanmıştır. Arazi, donanım, işletme, finansman ve fiyat değişimleri hesaba katılmamıştır.
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption("Veriler: Ekim 2026 itibarıyla erişilebilen kaynaklar · Hazırlayan: veridelisi")
