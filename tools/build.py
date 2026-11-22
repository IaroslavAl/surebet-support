#!/usr/bin/env python3
"""Builds the static support site from the texts below.

Run from the repository root:  python3 tools/build.py
Edit texts here (or the privacy fragments in tools/content), then rebuild and
commit the generated HTML. No dependencies beyond the Python standard library.
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://iaroslaval.github.io"
BASE = "/surebet-support/"  # path of the site on the host
APP_ID = "1667102550"
EMAIL = "beldin_dev@icloud.com"
UPDATED = "2026-11-21"
LANGS = ["en", "ru", "fr"]
ASSET_VERSION = "6"

BADGE_WIDTH = {"en": 119.66407, "ru": 119.66407, "fr": 126.50751}  # badge viewBox at height 40


def store_url(lang: str) -> str:
    return f"https://apps.apple.com/app/id{APP_ID}?ct=website-{lang}"


def asset(name: str) -> str:
    return f"{BASE}assets/{name}"


def exists(name: str) -> bool:
    return (ROOT / "assets" / name).exists()


def frenchify(text: str) -> str:
    """French spacing: narrow no-break space before ; ! ? and no-break space before :"""
    for mark in ("?", "!", ";"):
        text = text.replace(f" {mark}", f" {mark}")
    return text.replace(" :", " :")


# ---------------------------------------------------------------------------
# Texts
# ---------------------------------------------------------------------------

T: dict[str, dict] = {
    "en": {
        "locale": "en_US",
        "lang_name": "English",
        "title": "Surebet Calculator for iPhone and iPad — Surebet Stake Calculator",
        "description": (
            "Free surebet and arbitrage betting calculator for iPhone and iPad. "
            "Enter decimal odds for 2–20 outcomes to split your stake and see the "
            "profit and ROI for every outcome."
        ),
        "og_title": "Surebet Stake Calculator — surebet calculator for iPhone and iPad",
        "skip": "Skip to content",
        "nav": [("#how", "How it works"), ("#faq", "FAQ"), ("#support", "Support")],
        "lang_label": "Language",
        "eyebrow": "Free for iPhone and iPad",
        "h1": "Surebet and arbitrage betting calculator",
        "lead": (
            "Enter the odds and your total stake. The app splits the stake across "
            "the outcomes and shows your profit whichever one wins."
        ),
        "badge_alt": "Download on the App Store",
        "facts": ["Free", "iOS 16 or later", "No account"],
        "shot_alt": {
            "iphone": "Surebet Stake Calculator on iPhone: two outcomes and a 5% return",
            "mini": "The calculator on iPad in landscape",
            "duo": "The calculator on an unfolded iPhone Duo",
        },
        "how_kicker": "How it works",
        "how_h2": "Split a stake in three steps",
        "how_lead": "The same calculation a spreadsheet would do, without the spreadsheet.",
        "steps": [
            ("Choose 2 to 20 outcomes", "Set how many outcomes the event has: a tennis match has two, a football match has three."),
            ("Enter the decimal odds", "Type each bookmaker’s odds for its outcome. The result updates as you type."),
            ("Enter your total stake", "The calculator splits it so every outcome returns about the same payout, and shows the profit and ROI."),
        ],
        "example_title": "Example: two outcomes, total stake 1,000",
        "labels": {"total": "Total stake", "roi": "Min. ROI", "outcome": "Outcome", "odds": "Odds", "stake": "Stake", "profit": "Profit"},
        "example_note": "Whichever outcome wins, the payout is <strong>1,047.62</strong>: a profit of 47.62, or 4.76% of the total stake.",
        "modes_kicker": "Calculation modes",
        "modes_h2": "Three ways to calculate",
        "modes_lead": "Pick the mode that matches how you place bets. You can switch at any time.",
        "default_tag": "Default",
        "modes": [
            ("From a total stake", "Enter the total amount. The calculator splits it across all outcomes."),
            ("From one stake", "Select an outcome and enter your stake on it. The calculator works out the other stakes and the total."),
            ("Your own stakes", "Enter a stake for each outcome. The calculator adds them up and shows the profit or loss for each result."),
        ],
        "features_kicker": "Made for iPhone and iPad",
        "features_h2": "Everything for a quick check",
        "features_lead": "A focused calculator with a clean interface that follows Apple’s design.",
        "features": [
            ("2 to 20 outcomes", "From simple two-way markets to events with many outcomes."),
            ("Profit for every outcome", "See the result for each outcome and the minimum ROI before you place a bet."),
            ("8 languages", "English, French, German, Greek, Italian, Portuguese, Russian and Spanish."),
            ("Light and dark theme", "Follows your system setting, or stays light or dark."),
            ("No account", "Open the app and calculate. Calculations run on your device."),
            ("iPhone and iPad", "Works on iPhone and iPad with iOS and iPadOS 16 or later."),
        ],
        "faq_kicker": "FAQ",
        "faq_h2": "Questions about surebets and the app",
        "faq": [
            ("What is a surebet?", [
                "A surebet, or arbitrage bet, is a situation where the odds from different bookmakers on every outcome of an event let you split your stakes so that any outcome returns more than you staked in total.",
                "With decimal odds this happens when the sum of 1 ÷ odds over all outcomes is less than 1. For odds of 2.20 and 2.00 the sum is 0.9545, so a surebet exists.",
            ]),
            ("How does the calculator split the stake?", [
                "In total-stake mode each outcome gets a share proportional to 1 ÷ its odds, so the payouts come out almost equal. Stakes are rounded to cents.",
                "Min. ROI is the result for the least profitable outcome as a percentage of the total stake. In the example above it is 1 ÷ 0.9545 − 1 ≈ 4.76%.",
            ]),
            ("Does the app find surebets or connect to bookmakers?", [
                "No. The app does not fetch live odds, connect to bookmakers or detect arbitrage automatically. It calculates the result from the numbers you enter, so you can check an opportunity quickly.",
            ]),
            ("Is the profit guaranteed?", [
                "No. Odds can change before your bet is accepted, bookmakers can limit or void bets, and payouts can be rounded. Check each bookmaker’s rules before betting.",
                "Betting is for adults only and is not legal everywhere. The app is rated 17+ on the App Store.",
            ]),
            ("Which odds format does it use?", [
                "Decimal odds, such as 2.20 or 1.85. Enter them with a dot or a comma: the app uses your device’s number format.",
            ]),
            ("Do I need an account or an internet connection?", [
                "No account is needed. Calculations run on your device, so the calculator works without a connection.",
            ]),
            ("Is the app free?", [
                "Yes. Surebet Stake Calculator is free on the App Store.",
            ]),
            ("What data does the app collect?", [
                "The app uses Firebase and AppMetrica for usage statistics and crash reports. Calculation events do not include the odds or stakes you enter. Details are in the <a href=\"{privacy}\">privacy policy</a>.",
            ]),
        ],
        "support_kicker": "Support",
        "support_h2": "Contact the developer",
        "support_text": "Questions, bugs or ideas: write to me directly. To help me reproduce a problem, include the app version, your device model and the numbers you entered.",
        "support_button": "Email the developer",
        "privacy": "Privacy policy",
        "final_h2": "Check your next surebet in seconds",
        "final_text": "Surebet Stake Calculator is free on the App Store for iPhone and iPad.",
        "footer_disclaimer": "The app only calculates stakes. It does not accept bets, is not affiliated with any bookmaker and does not guarantee profit.",
        "trademarks": "Apple, the Apple logo, iPhone and iPad are trademarks of Apple Inc., registered in the U.S. and other countries and regions. App Store is a service mark of Apple Inc.",
        "footer_dev": "Developer",
        "back": "Back to the app page",
        "privacy_title": "Privacy policy · Surebet Stake Calculator",
        "privacy_description": "How Surebet Stake Calculator and this website handle data: usage statistics, crash reports, email support and your choices.",
        "notfound_title": "Page not found",
        "notfound_text": "This page does not exist.",
        "home": "Surebet Stake Calculator",
        "jsonld_desc": "Surebet and arbitrage betting calculator: split a stake across 2–20 outcomes and see the profit and ROI for each.",
        "decimal": ".",
        "group": ",",
        "percent": "{}%",
    },
    "ru": {
        "locale": "ru_RU",
        "lang_name": "Русский",
        "title": "Калькулятор вилок для iPhone и iPad — Surebet Stake Calculator",
        "description": (
            "Бесплатный калькулятор букмекерских вилок для iPhone и iPad. Введите "
            "коэффициенты для 2–20 исходов: приложение распределит ставки и покажет "
            "прибыль и доходность по каждому исходу."
        ),
        "og_title": "Surebet Stake Calculator — калькулятор вилок для iPhone и iPad",
        "skip": "Перейти к содержанию",
        "nav": [("#how", "Как это работает"), ("#faq", "Вопросы"), ("#support", "Поддержка")],
        "lang_label": "Язык",
        "eyebrow": "Бесплатно для iPhone и iPad",
        "h1": "Калькулятор букмекерских вилок",
        "lead": (
            "Введите коэффициенты и общую сумму. Приложение распределит её между "
            "исходами и покажет прибыль при любом результате."
        ),
        "badge_alt": "Загрузите в App Store",
        "facts": ["Бесплатно", "iOS 16 и новее", "Без регистрации"],
        "shot_alt": {
            "iphone": "Surebet Stake Calculator на iPhone: два исхода и доходность 5 %",
            "mini": "Калькулятор на горизонтальном iPad",
            "duo": "Калькулятор на раскрытом iPhone Duo",
        },
        "how_kicker": "Как это работает",
        "how_h2": "Расчёт вилки за три шага",
        "how_lead": "Тот же расчёт, что в таблице, только без таблицы.",
        "steps": [
            ("Выберите от 2 до 20 исходов", "Укажите, сколько исходов у события: у теннисного матча их два, у футбольного — три."),
            ("Введите коэффициенты", "Укажите коэффициент букмекера для каждого исхода. Результат обновляется сразу."),
            ("Введите общую сумму", "Калькулятор распределит её так, чтобы выплата по любому исходу была почти одинаковой, и покажет прибыль и доходность."),
        ],
        "example_title": "Пример: два исхода, сумма ставок 1\u00a0000",
        "labels": {"total": "Сумма ставок", "roi": "Мин. доходность", "outcome": "Исход", "odds": "Коэффициент", "stake": "Ставка", "profit": "Прибыль"},
        "example_note": "Какой бы исход ни сыграл, выплата составит <strong>1 047,62</strong>: прибыль 47,62, или 4,76 % от суммы ставок.",
        "modes_kicker": "Режимы расчёта",
        "modes_h2": "Три способа посчитать",
        "modes_lead": "Выберите режим под то, как вы ставите. Переключаться можно в любой момент.",
        "default_tag": "По умолчанию",
        "modes": [
            ("От общей суммы", "Введите общую сумму. Калькулятор распределит её между всеми исходами."),
            ("От одной ставки", "Отметьте исход и введите ставку на него. Калькулятор рассчитает остальные ставки и общую сумму."),
            ("Свои ставки", "Введите ставку на каждый исход. Калькулятор сложит их и покажет прибыль или убыток для каждого результата."),
        ],
        "features_kicker": "Для iPhone и iPad",
        "features_h2": "Всё для быстрой проверки",
        "features_lead": "Простой калькулятор с аккуратным интерфейсом в стиле Apple.",
        "features": [
            ("От 2 до 20 исходов", "От простых рынков на два исхода до событий с множеством исходов."),
            ("Прибыль по каждому исходу", "Результат для каждого исхода и минимальная доходность до того, как вы сделаете ставку."),
            ("8 языков", "Русский, английский, немецкий, греческий, испанский, итальянский, португальский и французский."),
            ("Светлая и тёмная тема", "Следует настройке системы или остаётся светлой либо тёмной."),
            ("Без регистрации", "Откройте приложение и считайте. Расчёт выполняется на устройстве."),
            ("iPhone и iPad", "Работает на iPhone и iPad с iOS и iPadOS 16 и новее."),
        ],
        "faq_kicker": "Вопросы",
        "faq_h2": "Частые вопросы о вилках и приложении",
        "faq": [
            ("Что такое букмекерская вилка?", [
                "Вилка (surebet, арбитражная ставка) — ситуация, когда коэффициенты разных букмекеров на все исходы события позволяют распределить ставки так, что любой исход принесёт больше, чем сумма всех ставок.",
                "Для десятичных коэффициентов вилка есть, если сумма 1 ÷ коэффициент по всем исходам меньше 1. Для коэффициентов 2,20 и 2,00 сумма равна 0,9545, значит, вилка есть.",
            ]),
            ("Как калькулятор распределяет сумму?", [
                "В режиме общей суммы каждому исходу достаётся доля, пропорциональная 1 ÷ его коэффициент, поэтому выплаты получаются почти равными. Ставки округляются до копеек.",
                "Мин. доходность — результат при наименее выгодном исходе в процентах от суммы ставок. В примере выше это 1 ÷ 0,9545 − 1 ≈ 4,76 %.",
            ]),
            ("Приложение само ищет вилки или подключается к букмекерам?", [
                "Нет. Приложение не загружает коэффициенты в реальном времени, не подключается к букмекерам и не ищет вилки автоматически. Оно считает результат по числам, которые вы вводите, чтобы быстро проверить возможность.",
            ]),
            ("Прибыль гарантирована?", [
                "Нет. Коэффициент может измениться до того, как ставку примут, букмекер может ограничить или аннулировать ставку, а выплату — округлить. Перед ставкой проверьте правила каждого букмекера.",
                "Ставки разрешены только совершеннолетним и не во всех странах. В App Store у приложения возрастной рейтинг 17+.",
            ]),
            ("Какой формат коэффициентов?", [
                "Десятичный, например 2,20 или 1,85. Вводите через запятую или точку: приложение использует числовой формат устройства.",
            ]),
            ("Нужны ли регистрация и интернет?", [
                "Регистрация не нужна. Расчёт выполняется на устройстве, поэтому калькулятор работает и без интернета.",
            ]),
            ("Приложение бесплатное?", [
                "Да. Surebet Stake Calculator бесплатен в App Store.",
            ]),
            ("Какие данные собирает приложение?", [
                "Приложение использует Firebase и AppMetrica для статистики использования и отчётов о сбоях. События расчёта не содержат введённых коэффициентов и ставок. Подробности — в <a href=\"{privacy}\">политике конфиденциальности</a>.",
            ]),
        ],
        "support_kicker": "Поддержка",
        "support_h2": "Связаться с разработчиком",
        "support_text": "Вопросы, ошибки, идеи — пишите мне напрямую. Чтобы я быстрее разобрался с проблемой, укажите версию приложения, модель устройства и числа, которые вы вводили.",
        "support_button": "Написать разработчику",
        "privacy": "Политика конфиденциальности",
        "final_h2": "Проверьте следующую вилку за секунды",
        "final_text": "Surebet Stake Calculator бесплатен в App Store для iPhone и iPad.",
        "footer_disclaimer": "Приложение только рассчитывает ставки. Оно не принимает ставки, не связано с букмекерами и не гарантирует прибыль.",
        "trademarks": "Apple, логотип Apple, iPhone и iPad — товарные знаки Apple Inc., зарегистрированные в США и других странах и регионах. App Store — знак обслуживания Apple Inc.",
        "footer_dev": "Разработчик",
        "back": "К странице приложения",
        "privacy_title": "Политика конфиденциальности · Surebet Stake Calculator",
        "privacy_description": "Как Surebet Stake Calculator и этот сайт обращаются с данными: статистика использования, отчёты о сбоях, поддержка по почте и ваши права.",
        "notfound_title": "Страница не найдена",
        "notfound_text": "Такой страницы нет.",
        "home": "Surebet Stake Calculator",
        "jsonld_desc": "Калькулятор букмекерских вилок: распределите ставку между 2–20 исходами и посмотрите прибыль и доходность по каждому.",
        "decimal": ",",
        "group": " ",
        "percent": "{} %",
    },
    "fr": {
        "locale": "fr_FR",
        "lang_name": "Français",
        "title": "Calculateur de surebet pour iPhone et iPad — Surebet Stake Calculator",
        "description": (
            "Calculatrice de surebet et de paris d’arbitrage gratuite pour iPhone et "
            "iPad. Saisissez les cotes de 2 à 20 issues pour répartir votre mise et "
            "voir le gain et le rendement de chaque issue."
        ),
        "og_title": "Surebet Stake Calculator — calculateur de surebet pour iPhone et iPad",
        "skip": "Aller au contenu",
        "nav": [("#how", "Fonctionnement"), ("#faq", "Questions"), ("#support", "Assistance")],
        "lang_label": "Langue",
        "eyebrow": "Gratuit pour iPhone et iPad",
        "h1": "Calculateur de surebet et de paris d’arbitrage",
        "lead": (
            "Saisissez les cotes et votre mise totale. L’app la répartit entre les "
            "issues et affiche votre gain, quelle que soit l’issue gagnante."
        ),
        "badge_alt": "Télécharger dans l’App Store",
        "facts": ["Gratuit", "iOS 16 ou version ultérieure", "Sans compte"],
        "shot_alt": {
            "iphone": "Surebet Stake Calculator sur iPhone : deux issues et un rendement de 5 %",
            "mini": "Le calculateur sur iPad à l’horizontale",
            "duo": "Le calculateur sur un iPhone Duo déplié",
        },
        "how_kicker": "Fonctionnement",
        "how_h2": "Répartir une mise en trois étapes",
        "how_lead": "Le même calcul qu’un tableur, sans le tableur.",
        "steps": [
            ("Choisissez de 2 à 20 issues", "Indiquez le nombre d’issues de l’événement : deux pour un match de tennis, trois pour un match de football."),
            ("Saisissez les cotes décimales", "Indiquez la cote de chaque bookmaker pour son issue. Le résultat se met à jour pendant la saisie."),
            ("Saisissez votre mise totale", "Le calculateur la répartit pour que chaque issue rapporte presque le même montant, et affiche le gain et le rendement."),
        ],
        "example_title": "Exemple : deux issues, mise totale de 1\u202f000",
        "labels": {"total": "Mise totale", "roi": "Rendement min.", "outcome": "Issue", "odds": "Cote", "stake": "Mise", "profit": "Gain net"},
        "example_note": "Quelle que soit l’issue gagnante, le montant versé est de <strong>1 047,62</strong> : un gain de 47,62, soit 4,76 % de la mise totale.",
        "modes_kicker": "Modes de calcul",
        "modes_h2": "Trois façons de calculer",
        "modes_lead": "Choisissez le mode adapté à votre façon de parier. Vous pouvez en changer à tout moment.",
        "default_tag": "Par défaut",
        "modes": [
            ("À partir du total", "Saisissez le montant total. Le calculateur le répartit entre toutes les issues."),
            ("À partir d’une mise", "Cochez une issue et saisissez votre mise. Le calculateur détermine les autres mises et le total."),
            ("Vos propres mises", "Saisissez une mise par issue. Le calculateur les additionne et affiche le gain ou la perte pour chaque résultat."),
        ],
        "features_kicker": "Pour iPhone et iPad",
        "features_h2": "Tout pour vérifier rapidement",
        "features_lead": "Un calculateur simple, avec une interface soignée dans le style d’Apple.",
        "features": [
            ("De 2 à 20 issues", "Des marchés simples à deux issues jusqu’aux événements à nombreuses issues."),
            ("Le gain de chaque issue", "Le résultat de chaque issue et le rendement minimal avant de parier."),
            ("8 langues", "Français, anglais, allemand, espagnol, grec, italien, portugais et russe."),
            ("Thème clair et sombre", "Suit le réglage du système, ou reste clair ou sombre."),
            ("Sans compte", "Ouvrez l’app et calculez. Les calculs se font sur votre appareil."),
            ("iPhone et iPad", "Fonctionne sur iPhone et iPad avec iOS et iPadOS 16 ou version ultérieure."),
        ],
        "faq_kicker": "Questions",
        "faq_h2": "Questions sur les surebets et l’app",
        "faq": [
            ("Qu’est-ce qu’un surebet ?", [
                "Un surebet, ou pari d’arbitrage, est une situation où les cotes de différents bookmakers sur toutes les issues d’un événement permettent de répartir les mises pour que chaque issue rapporte plus que le total misé.",
                "Avec des cotes décimales, c’est le cas lorsque la somme de 1 ÷ cote sur toutes les issues est inférieure à 1. Pour des cotes de 2,20 et 2,00, la somme vaut 0,9545 : il y a donc un surebet.",
            ]),
            ("Comment la mise est-elle répartie ?", [
                "En mode mise totale, chaque issue reçoit une part proportionnelle à 1 ÷ sa cote, si bien que les montants versés sont presque identiques. Les mises sont arrondies au centime.",
                "Le rendement min. correspond au résultat de l’issue la moins favorable, en pourcentage de la mise totale. Dans l’exemple ci-dessus : 1 ÷ 0,9545 − 1 ≈ 4,76 %.",
            ]),
            ("L’app trouve-t-elle les surebets ou se connecte-t-elle aux bookmakers ?", [
                "Non. L’app ne récupère pas les cotes en direct, ne se connecte pas aux bookmakers et ne détecte pas les arbitrages automatiquement. Elle calcule le résultat à partir des nombres que vous saisissez, pour vérifier rapidement une opportunité.",
            ]),
            ("Le gain est-il garanti ?", [
                "Non. Une cote peut changer avant que votre pari soit accepté, un bookmaker peut limiter ou annuler un pari, et les montants versés peuvent être arrondis. Vérifiez les règles de chaque bookmaker avant de parier.",
                "Les paris sont réservés aux adultes et ne sont pas autorisés partout. L’app est classée 17+ sur l’App Store.",
            ]),
            ("Quel format de cotes ?", [
                "Les cotes décimales, comme 2,20 ou 1,85. Saisissez-les avec une virgule ou un point : l’app utilise le format numérique de votre appareil.",
            ]),
            ("Faut-il un compte ou une connexion Internet ?", [
                "Aucun compte n’est nécessaire. Les calculs se font sur votre appareil, le calculateur fonctionne donc sans connexion.",
            ]),
            ("L’app est-elle gratuite ?", [
                "Oui. Surebet Stake Calculator est gratuit sur l’App Store.",
            ]),
            ("Quelles données l’app collecte-t-elle ?", [
                "L’app utilise Firebase et AppMetrica pour les statistiques d’utilisation et les rapports de plantage. Les événements de calcul ne contiennent ni les cotes ni les mises saisies. Détails dans la <a href=\"{privacy}\">politique de confidentialité</a>.",
            ]),
        ],
        "support_kicker": "Assistance",
        "support_h2": "Contacter le développeur",
        "support_text": "Questions, bugs ou idées : écrivez-moi directement. Pour m’aider à reproduire un problème, indiquez la version de l’app, le modèle de votre appareil et les nombres saisis. Je réponds en anglais ou en russe.",
        "support_button": "Écrire au développeur",
        "privacy": "Politique de confidentialité",
        "final_h2": "Vérifiez votre prochain surebet en quelques secondes",
        "final_text": "Surebet Stake Calculator est gratuit sur l’App Store pour iPhone et iPad.",
        "footer_disclaimer": "L’app calcule uniquement les mises. Elle n’accepte pas de paris, n’est affiliée à aucun bookmaker et ne garantit aucun gain.",
        "trademarks": "Apple, le logo Apple, iPhone et iPad sont des marques d’Apple Inc., déposées aux États-Unis et dans d’autres pays et régions. App Store est une marque de service d’Apple Inc.",
        "footer_dev": "Développeur",
        "back": "Retour à la page de l’app",
        "privacy_title": "Politique de confidentialité · Surebet Stake Calculator",
        "privacy_description": "Comment Surebet Stake Calculator et ce site traitent les données : statistiques d’utilisation, rapports de plantage, assistance par e-mail et vos choix.",
        "notfound_title": "Page introuvable",
        "notfound_text": "Cette page n’existe pas.",
        "home": "Surebet Stake Calculator",
        "jsonld_desc": "Calculateur de surebet et de paris d’arbitrage : répartissez une mise entre 2 et 20 issues et voyez le gain et le rendement de chacune.",
        "decimal": ",",
        "group": " ",
        "percent": "{} %",
    },
}

# Icons for cards: simple strokes, 24×24.
ICONS = {
    "total": '<path d="M4 6h16M12 6v4M12 10l-6 7M12 10v7M12 10l6 7"/><circle cx="6" cy="18.5" r="1.5"/><circle cx="12" cy="18.5" r="1.5"/><circle cx="18" cy="18.5" r="1.5"/>',
    "pin": '<path d="M9 4h6l-1 6 3 3H7l3-3-1-6zM12 13v7"/>',
    "manual": '<path d="M5 7h9M18 7h1M5 12h3M12 12h7M5 17h11M20 17h-1"/><circle cx="16" cy="7" r="2"/><circle cx="10" cy="12" r="2"/><circle cx="18" cy="17" r="2"/>',
    "outcomes": '<rect x="4" y="4" width="7" height="7" rx="2"/><rect x="13" y="4" width="7" height="7" rx="2"/><rect x="4" y="13" width="7" height="7" rx="2"/><path d="M16.5 14v5M14 16.5h5"/>',
    "profit": '<path d="M4 18l5-5 4 3 7-8"/><path d="M15 8h5v5"/>',
    "lang": '<circle cx="12" cy="12" r="8"/><path d="M4 12h16M12 4c2.5 2.5 3.5 5 3.5 8s-1 5.5-3.5 8c-2.5-2.5-3.5-5-3.5-8s1-5.5 3.5-8z"/>',
    "theme": '<circle cx="12" cy="12" r="8"/><path d="M12 4a8 8 0 0 1 0 16z" fill="currentColor"/>',
    "lock": '<rect x="5" y="10.5" width="14" height="9.5" rx="2.5"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    "devices": '<rect x="3" y="5" width="13" height="14" rx="2"/><rect x="15" y="9" width="6" height="11" rx="1.5"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="3"/><path d="M4 7l8 6 8-6"/>',
}
MODE_ICONS = ["total", "pin", "manual"]
FEATURE_ICONS = ["outcomes", "profit", "lang", "theme", "lock", "devices"]


def icon(name: str) -> str:
    return (
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" '
        f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def num(lang: str, value: float, digits: int = 2) -> str:
    s = f"{value:,.{digits}f}"
    s = s.replace(",", "\x00").replace(".", T[lang]["decimal"]).replace("\x00", T[lang]["group"])
    return s


def page_url(lang: str, kind: str) -> str:
    return f"{SITE}{BASE}{lang}/" + ("privacy/" if kind == "privacy" else "")


def picture(lang: str, name: str, alt: str, width: int, height: int, lazy: bool) -> str:
    base = f"{name}-{lang}" if exists(f"{name}-{lang}.webp") else f"{name}-en"
    dark = f"{base}-dark.webp"
    source = (
        f'<source media="(prefers-color-scheme: dark)" srcset="{asset(dark)}?v={ASSET_VERSION}" />'
        if exists(dark)
        else ""
    )
    loading = ' loading="lazy"' if lazy else ""
    return (
        f"<picture>{source}<img src=\"{asset(base + '.webp')}?v={ASSET_VERSION}\" alt=\"{esc(alt)}\" "
        f'width="{width}" height="{height}"{loading} decoding="async" /></picture>'
    )


def badge(lang: str, eager: bool = True, adaptive: bool = False) -> str:
    t = T[lang]
    h = 54
    w = round(BADGE_WIDTH[lang] * h / 40)
    dark = (
        f'<source media="(prefers-color-scheme: dark)" srcset="{asset(f"badges/{lang}-white.svg")}" />'
        if adaptive
        else ""
    )
    loading = "" if eager else ' loading="lazy"'
    return (
        f'<a class="store-badge" href="{esc(store_url(lang))}">'
        f'<picture>{dark}<img src="{asset(f"badges/{lang}-black.svg")}" alt="{esc(t["badge_alt"])}" '
        f'width="{w}" height="{h}"{loading} /></picture></a>'
    )


def head(lang: str, kind: str, title: str, description: str, *, noindex: bool = False, canonical: str | None = None) -> str:
    t = T[lang]
    canonical = canonical or page_url(lang, kind)
    alternates = "".join(
        f'\n    <link rel="alternate" hreflang="{l}" href="{page_url(l, kind)}" />' for l in LANGS
    ) + f'\n    <link rel="alternate" hreflang="x-default" href="{page_url("en", kind)}" />'
    og_locales = "".join(
        f'\n    <meta property="og:locale:alternate" content="{T[l]["locale"]}" />' for l in LANGS if l != lang
    )
    robots = '\n    <meta name="robots" content="noindex" />' if noindex else ""
    jsonld = ""
    if kind == "home":
        data = {
            "@context": "https://schema.org",
            "@type": "MobileApplication",
            "name": "Surebet Stake Calculator",
            "description": t["jsonld_desc"],
            "operatingSystem": "iOS 16.0 or later, iPadOS 16.0 or later",
            "applicationCategory": "FinanceApplication",
            "inLanguage": lang,
            "url": page_url(lang, "home"),
            "downloadUrl": f"https://apps.apple.com/app/id{APP_ID}",
            "installUrl": f"https://apps.apple.com/app/id{APP_ID}",
            "image": f"{SITE}{asset('icon-256.png')}",
            "screenshot": f"{SITE}{asset(('iphone-' + lang if exists('iphone-' + lang + '.webp') else 'iphone-en') + '.webp')}",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
            "author": {"@type": "Person", "name": "Iaroslav Beldin", "email": f"mailto:{EMAIL}"},
        }
        jsonld = (
            '\n    <script type="application/ld+json">'
            + json.dumps(data, ensure_ascii=False, separators=(",", ":"))
            + "</script>"
        )
    og_image = f"{SITE}{asset(f'og-{lang}.jpg')}"
    return f"""<!doctype html>
<html lang="{lang}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover" />
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(description)}" />{robots}
    <link rel="canonical" href="{canonical}" />{alternates}
    <meta name="apple-itunes-app" content="app-id={APP_ID}" />
    <meta name="theme-color" content="#137a41" media="(prefers-color-scheme: light)" />
    <meta name="theme-color" content="#0f5530" media="(prefers-color-scheme: dark)" />
    <meta property="og:type" content="website" />
    <meta property="og:site_name" content="Surebet Stake Calculator" />
    <meta property="og:title" content="{esc(t['og_title'] if kind == 'home' else title)}" />
    <meta property="og:description" content="{esc(description)}" />
    <meta property="og:url" content="{canonical}" />
    <meta property="og:image" content="{og_image}" />
    <meta property="og:image:width" content="1200" />
    <meta property="og:image:height" content="630" />
    <meta property="og:locale" content="{t['locale']}" />{og_locales}
    <meta name="twitter:card" content="summary_large_image" />
    <link rel="icon" type="image/png" sizes="64x64" href="{asset('icon-64.png')}" />
    <link rel="apple-touch-icon" href="{asset('icon.png')}" />
    <link rel="stylesheet" href="{asset('site.css')}?v={ASSET_VERSION}" />{jsonld}
  </head>
"""


def header(lang: str, kind: str) -> str:
    t = T[lang]
    nav = ""
    if kind == "home":
        nav = '<nav class="site-nav" aria-label="{}">{}</nav>'.format(
            esc(t["home"]), "".join(f'<a href="{h}">{esc(label)}</a>' for h, label in t["nav"])
        )
    links = "".join(
        f'<a href="{BASE}{l}/' + ("privacy/" if kind == "privacy" else "") + f'" lang="{l}" hreflang="{l}" '
        f'title="{T[l]["lang_name"]}"' + (' aria-current="page"' if l == lang else "") + f">{l.upper()}</a>"
        for l in LANGS
    )
    return f"""  <body>
    <a class="skip" href="#main">{esc(t['skip'])}</a>
    <header class="site-header">
      <div class="wrap">
        <a class="brand" href="{BASE}{lang}/"><img src="{asset('icon-64.png')}" alt="" width="32" height="32" />Surebet Stake Calculator</a>
        {nav}
        <div class="lang" role="group" aria-label="{esc(t['lang_label'])}">{links}</div>
      </div>
    </header>
"""


def footer(lang: str) -> str:
    t = T[lang]
    langs = "".join(
        f'<li><a href="{BASE}{l}/" lang="{l}" hreflang="{l}">{T[l]["lang_name"]}</a></li>' for l in LANGS if l != lang
    )
    return f"""    <footer class="site-footer">
      <div class="wrap">
        <div class="footer-grid">
          <div>
            <div class="footer-brand"><img src="{asset('icon-64.png')}" alt="" width="28" height="28" loading="lazy" />Surebet Stake Calculator</div>
            <p>{esc(t['footer_disclaimer'])}</p>
          </div>
          <ul class="footer-links">
            <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
            <li><a href="{BASE}{lang}/privacy/">{esc(t['privacy'])}</a></li>
            <li><a href="{esc(store_url(lang))}">App Store</a></li>
            {langs}
          </ul>
        </div>
        <div class="fineprint">
          <p>© 2026 Iaroslav Beldin</p>
          <p>{esc(t['trademarks'])}</p>
        </div>
      </div>
    </footer>
  </body>
</html>
"""


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------


def home(lang: str, canonical: str | None = None) -> str:
    t = {k: (frenchify(v) if lang == "fr" and isinstance(v, str) else v) for k, v in T[lang].items()}
    L = t["labels"]
    fr = (lambda s: frenchify(s)) if lang == "fr" else (lambda s: s)
    privacy = f"{BASE}{lang}/privacy/"

    steps = "".join(
        f"<li><h3>{esc(fr(a))}</h3><p>{esc(fr(b))}</p></li>" for a, b in t["steps"]
    )
    rows = ""
    for i, (odds, stake, profit) in enumerate([(2.20, 476.19, 47.62), (2.00, 523.81, 47.62)], 1):
        rows += (
            f'<tr><th scope="row"><span class="outcome-no" aria-label="{esc(L["outcome"])} {i}">{i}</span></th>'
            f'<td><span class="field">{num(lang, odds)}</span></td>'
            f'<td><span class="field field-out">{num(lang, stake)}</span></td>'
            f'<td><span class="field field-good">{num(lang, profit)}</span></td></tr>'
        )
    roi = t["percent"].format(num(lang, 4.76))
    modes = "".join(
        f'<li class="card"><span class="card-icon">{icon(MODE_ICONS[i])}</span>'
        + f"<h3>{esc(fr(a))}"
        + (f' <span class="tag">{esc(t["default_tag"])}</span>' if i == 0 else "")
        + f"</h3><p>{esc(fr(b))}</p></li>"
        for i, (a, b) in enumerate(t["modes"])
    )
    features = "".join(
        f'<li class="card"><span class="card-icon">{icon(FEATURE_ICONS[i])}</span><h3>{esc(fr(a))}</h3><p>{esc(fr(b))}</p></li>'
        for i, (a, b) in enumerate(t["features"])
    )
    faq = "".join(
        f"<details{' open' if i == 0 else ''}><summary>{esc(fr(q))}</summary><div>"
        + "".join(f"<p>{fr(p).format(privacy=privacy)}</p>" for p in answers)
        + "</div></details>"
        for i, (q, answers) in enumerate(t["faq"])
    )
    alt = {k: fr(v) for k, v in t["shot_alt"].items()}

    body = f"""    <main id="main">
      <section class="hero">
        <div class="wrap hero-grid">
          <div class="hero-copy">
            <img class="hero-icon" src="{asset('icon-256.png')}" alt="" width="72" height="72" />
            <p class="eyebrow">{esc(t['eyebrow'])}</p>
            <h1>{esc(t['h1'])}</h1>
            <p class="lead">{esc(t['lead'])}</p>
            <div class="cta">
              {badge(lang)}
              <ul class="facts">{''.join(f'<li>{esc(f)}</li>' for f in t['facts'])}</ul>
            </div>
          </div>
          <figure class="hero-visual">
            <div class="device-stage">
              <div class="device device-iphone"><span class="hardware">{picture(lang, 'iphone', alt['iphone'], 1000, 2175, False)}</span></div>
              <div class="device device-mini"><span class="hardware">{picture(lang, 'mini', alt['mini'], 1600, 1200, True)}</span></div>
              <div class="device device-duo"><span class="hardware">{picture(lang, 'duo', alt['duo'], 1600, 1126, True)}</span></div>
            </div>
          </figure>
        </div>
      </section>

      <section class="section" id="how" aria-labelledby="how-title">
        <div class="wrap how">
          <div>
            <div class="section-head">
              <p class="kicker">{esc(t['how_kicker'])}</p>
              <h2 id="how-title">{esc(t['how_h2'])}</h2>
              <p>{esc(t['how_lead'])}</p>
            </div>
            <ol class="steps">{steps}</ol>
          </div>
          <figure class="calc">
            <figcaption class="calc-title">{esc(t['example_title'])}</figcaption>
            <dl class="calc-total">
              <dt>{esc(L['total'])}</dt><dd><span class="field">{num(lang, 1000, 0)}</span></dd>
              <dt>{esc(L['roi'])}</dt><dd><span class="field field-good">{roi}</span></dd>
            </dl>
            <table class="calc-table">
              <caption>{esc(t['example_title'])}</caption>
              <colgroup><col class="n" /><col /><col /><col /></colgroup>
              <thead><tr><td></td><th scope="col">{esc(L['odds'])}</th><th scope="col">{esc(L['stake'])}</th><th scope="col">{esc(L['profit'])}</th></tr></thead>
              <tbody>{rows}</tbody>
            </table>
            <p class="calc-note">{t['example_note']}</p>
          </figure>
        </div>
      </section>

      <section class="section section-alt" id="modes" aria-labelledby="modes-title">
        <div class="wrap">
          <div class="section-head">
            <p class="kicker">{esc(t['modes_kicker'])}</p>
            <h2 id="modes-title">{esc(t['modes_h2'])}</h2>
            <p>{esc(t['modes_lead'])}</p>
          </div>
          <ul class="cards cards-3">{modes}</ul>
        </div>
      </section>

      <section class="section" id="features" aria-labelledby="features-title">
        <div class="wrap">
          <div class="section-head">
            <p class="kicker">{esc(t['features_kicker'])}</p>
            <h2 id="features-title">{esc(t['features_h2'])}</h2>
            <p>{esc(t['features_lead'])}</p>
          </div>
          <ul class="cards cards-3">{features}</ul>
        </div>
      </section>

      <section class="section section-alt" id="faq" aria-labelledby="faq-title">
        <div class="wrap faq-layout">
          <div class="section-head">
            <p class="kicker">{esc(t['faq_kicker'])}</p>
            <h2 id="faq-title">{esc(t['faq_h2'])}</h2>
          </div>
          <div class="faq">{faq}</div>
        </div>
      </section>

      <section class="section" id="support" aria-labelledby="support-title">
        <div class="wrap">
          <div class="support">
            <div>
              <p class="kicker">{esc(t['support_kicker'])}</p>
              <h2 id="support-title">{esc(t['support_h2'])}</h2>
              <p>{esc(t['support_text'])}</p>
            </div>
            <div class="support-actions">
              <a class="button" href="mailto:{EMAIL}">{icon('mail')}{esc(t['support_button'])}</a>
              <a class="mail" href="mailto:{EMAIL}">{EMAIL}</a>
              <a href="{privacy}">{esc(t['privacy'])}</a>
            </div>
          </div>
        </div>
      </section>

      <section class="section section-alt" aria-labelledby="final-title">
        <div class="wrap final">
          <img class="app-icon" src="{asset('icon-256.png')}" alt="" width="80" height="80" loading="lazy" />
          <h2 id="final-title">{esc(t['final_h2'])}</h2>
          <p>{esc(t['final_text'])}</p>
          {badge(lang, eager=False, adaptive=True)}
        </div>
      </section>
    </main>
"""
    return head(lang, "home", t["title"], t["description"], canonical=canonical) + header(lang, "home") + body + footer(lang)


def privacy_page(lang: str) -> str:
    t = T[lang]
    fragment = (ROOT / "tools" / "content" / f"privacy-{lang}.html").read_text()
    if lang == "fr":
        fragment = frenchify(fragment)
    body = f"""    <main id="main" class="wrap">
      <article class="policy">
        <a class="back" href="{BASE}{lang}/">← {esc(t['back'])}</a>
        {fragment.strip()}
      </article>
    </main>
"""
    return head(lang, "privacy", t["privacy_title"], t["privacy_description"]) + header(lang, "privacy") + body + footer(lang)


def not_found() -> str:
    t = T["en"]
    items = "".join(
        f'<p lang="{l}"><strong>{esc(T[l]["notfound_title"])}.</strong> {esc(T[l]["notfound_text"])} <a href="{BASE}{l}/">{esc(T[l]["back"])}</a></p>'
        for l in LANGS
    )
    body = f"""    <main id="main" class="wrap">
      <div class="notfound">
        <h1>404</h1>
        {items}
        {badge('en')}
      </div>
    </main>
"""
    return head("en", "404", "Page not found · Surebet Stake Calculator", t["description"], noindex=True) + header("en", "404") + body + footer("en")


def sitemap() -> str:
    urls = []
    for kind in ("home", "privacy"):
        for lang in LANGS:
            alts = "".join(
                f'\n    <xhtml:link rel="alternate" hreflang="{l}" href="{page_url(l, kind)}" />' for l in LANGS
            ) + f'\n    <xhtml:link rel="alternate" hreflang="x-default" href="{page_url("en", kind)}" />'
            urls.append(
                f"  <url>\n    <loc>{page_url(lang, kind)}</loc>\n    <lastmod>{UPDATED}</lastmod>{alts}\n  </url>"
            )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
        + "\n".join(urls)
        + "\n</urlset>\n"
    )


# Hero background: the App Store header's tiles of the icon's SF Symbols
# (plus, soccerball, tennisball.fill, equal). Sources in tools/symbols are the
# same exports as design/app-icon/symbols in the app repository.
SYMBOLS = {
    # name: (crop viewBox, glyph width and height in the 512-px icon quadrant)
    "plus": ("6.5 6.5 46.25 46.5", 236.72, 238),
    "soccerball": ("4.25 11.75 57.5 57.5", 300, 300),
    "tennisball.fill": ("4.25 11.75 57.5 57.5", 300, 300),
    "equal": ("6.5 4 39.25 23", 236, 138.29),
}
PATTERN_ORDER = ["plus", "soccerball", "tennisball.fill", "equal"]
PATTERN_PITCH = 120  # tile step; the repeating unit is 4 x 4 steps
PATTERN_TILE = 96
PATTERN_GLYPH = 0.72  # glyph size relative to the icon, as in the App Store header


def pattern() -> str:
    defs = []
    for name, (view_box, _, _) in SYMBOLS.items():
        src = (ROOT / "tools" / "symbols" / f"{name}.svg").read_text()
        transform = re.search(r"<g [^>]*transform='([^']+)'", src).group(1)
        d = " ".join(re.search(r" d='([^']+)'", src).group(1).split())
        defs.append(
            f'<symbol id="{name}" viewBox="{view_box}">'
            f'<path transform="{transform}" d="{d}"/></symbol>'
        )
    p, t = PATTERN_PITCH, PATTERN_TILE
    size = 4 * p
    scale = t / 512 * PATTERN_GLYPH
    tiles, glyphs = [], []
    for row in range(4):
        offset = (p // 2) * (row % 2)
        for col in range(-1, 5):
            x = offset + col * p + (p - t) / 2
            y = row * p + (p - t) / 2
            if x + t <= 0 or x >= size:
                continue
            name = PATTERN_ORDER[(col - row) % 4]
            _, w, h = SYMBOLS[name]
            gw, gh = w * scale, h * scale
            tiles.append(f'<rect x="{x:g}" y="{y:g}" width="{t}" height="{t}" rx="22"/>')
            glyphs.append(
                f'<use href="#{name}" x="{x + (t - gw) / 2:.2f}" y="{y + (t - gh) / 2:.2f}" '
                f'width="{gw:.2f}" height="{gh:.2f}"/>'
            )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">\n<defs>{"".join(defs)}</defs>\n'
        f'<g fill="#fff" fill-opacity=".06">{"".join(tiles)}</g>\n'
        f'<g fill="#fff" stroke="#fff" stroke-width="1" fill-opacity=".2" stroke-opacity=".2">'
        f'{"".join(glyphs)}</g>\n</svg>\n'
    )


def write(path: str, text: str) -> None:
    text = text.replace("App Store", "App\u00a0Store")
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text)
    print("wrote", path)


def main() -> None:
    for lang in LANGS:
        write(f"{lang}/index.html", home(lang))
        write(f"{lang}/privacy/index.html", privacy_page(lang))
    write("index.html", home("en", canonical=page_url("en", "home")))
    write("404.html", not_found())
    write("sitemap.xml", sitemap())
    write("assets/pattern.svg", pattern())


if __name__ == "__main__":
    main()
