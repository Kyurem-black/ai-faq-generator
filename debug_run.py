from backend.utils import generate_faqs
import json
c=('Anime refers to hand-drawn or computer-generated animation originating from Japan. '
   'Globally, the term specifically describes Japanese animation, characterized by colorful artwork, '
   'expressive and exaggerated characters, and diverse themes suitable for all ages. '
   'Anime often includes genres like action, romance, comedy, and fantasy.')
print('Calling generate_faqs...')
res = generate_faqs('Anime', c, num=5)
print(json.dumps(res, ensure_ascii=False, indent=2))
