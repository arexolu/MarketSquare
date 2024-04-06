from .app import app
from .products.model import Product

# Seed Products Table
_products = [
    {
        "name": "SAMBA OG SHOES",
        "description": "A true icon first released in 1950, this reissue of the adidas Samba OG shoes celebrates the sneaker's sporty roots while tailoring its timeless style for today. Smooth leather envelops the foot in retro comfort while reinforced details at the toe and eyelets subtly signal its football heritage. An archival classic reborn, this pair continues the Samba legacy one stylish step at a time.",
        "price": 109.99,
        "units_available": 200,
        "image": "https://assets.adidas.com/images/h_840,f_auto,q_auto,fl_lossy,c_fill,g_auto/673dd32eabf3476f9b9605d91616ee49_9366/Samba_OG_Shoes_Grey_ID0493_01_standard.jpg"
    },
    {
        "name": "SUPERSTAR XLG SHOES",
        "description": "The adidas Superstar XLG shoes bring an edge to an iconic court classic. With a camouflage ripstop upper and gold foil accents, these kicks are ready to traverse the streets. First making their mark on the hardwood, the adidas Superstar shoes have spent over 50 years infiltrating street culture and earning status as an everyday essential. The distinctive shell toe, originally engineered for protection, is now a signature design detail and symbol of a shoe that's rooted in sport but embraced by lifestyle legends. For over 50 years, this is the go-to for those who shape sports and style.",
        "price": 134.99,
        "units_available": 250,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/932062bb405b43bdb575657044ef2ade_9366/Superstar_XLG_Shoes_Green_IF3689_01_standard.jpg"
    },
    {
        "name": "NMD_W1 SHOES",
        "description": "The adidas NMD_W1 shoes are all about stylish practicality. This pair takes core characteristics of the adidas NMD_R1 while adding stylistic modifications. The midsole plugs take on a more sleek shape, and the responsive BOOST midsole is enlarged to give the silhouette a platform look. Add on the signature textile upper and maximize your comfort with each step. The futuristic look in a range of colors makes this pair a staple in any rotation.",
        "price": 189.99,
        "units_available": 200,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/63d563528cb64345a6f1985089a4003f_9366/NMD_W1_Shoes_Brown_IE8211_01_standard.jpg"
    },
    {
        "name": "SUPERSTAR SHOES",
        "description": "Back in the day they were the go-to basketball low top. Today they're a streetwear icon. These juniors' shoes celebrate 50 years of the adidas Superstar. From the classic shell toe to the serrated 3-Stripes, this anniversary edition honors an unmistakable adidas design. Built on a comfortable rubber cupsole, they look fresh and fun no matter the color.",
        "price": 99.99,
        "units_available": 300,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/a5222393204c4190b5a4ab0000b325cc_9366/Superstar_Shoes_Black_EF5398_01_standard.jpg"
    },
    {
        "name": "CAMPUS 00S SHOES",
        "description": "Although they made their debut on the hardwood, the adidas Campus shoes were quickly adopted just about everywhere else. With this pair, we move the iconic silhouette in another direction and add modern materials, colors and proportions. They're done with a premium leather upper lined with soft textile terry fabric, with all of it riding on an off-white midsole — a clear connect to the Campus legacy.",
        "price": 54.99,
        "units_available": 400,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/ce738cbe5342421996feaf5001044964_9366/Campus_00s_Shoes_Grey_HQ8707_01_standard.jpg"
    },
    {
        "name": "OZMILLEN SHOES",
        "description": "For the free-thinker who forges a path all their own, the adidas OZMILLEN shoes lead where the crowd won't follow. Inspired by the radical '90s Ozweego runner, these low-profile shoes excite with a split mesh tongue, an iconic toe box and TPU 3-Stripes with a peekaboo quarter window. The reflective overlays and underlays in mesh and synthetic leather add futuristic flair. Adiplus cushioning delivers undeniable comfort so you can power through your day in versatile, energetic style.",
        "price": 79.99,
        "units_available": 100,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/c8c56ab6b0cf4e3a9b261acf2318e6ab_9366/OZMILLEN_Shoes_Black_IE5842_01_standard.jpg"
    },
    {
        "name": "ADIFOM CLIMACOOL SHOES",
        "description": "These adidas shoes put innovation at the center of their design. Made for keep-cool comfort, they're like a breath of fresh air for your feet thanks to ventilation that helps regulate warmth. Soft cushioning makes every step feel plush, and an interior mesh lining fits like a sock. A bio-based material shapes the outer shell into rugged style made modern.",
        "price": 204.99,
        "units_available": 160,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/ad884f7eec5a430985e64c5dea95cf7e_9366/Adifom_Climacool_Shoes_Black_IF3902_01_standard.jpg"
    },
    {
        "name": "STAN SMITH LUX SHOES",
        "description": "The time-honored silhouette gets an update in the Stan Smith Lux. With a clean and genderless look that nods to the OG, this iteration is effortlessly elevated with premium details. The court-inspired shoe is crafted entirely from buttery-soft leather, from the inner lining to the extra leather patch in the heel that provides heightened comfort and durability. The foil branding on the tongue is a simple yet elegant finish.",
        "price": 146.99,
        "units_available": 180,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/38d40c824ed84b12b641af17005a5dec_9366/Stan_Smith_Lux_Shoes_Black_HQ6787_HM1.jpg"
    },
    {
        "name": "FORUM 84 LOW CL SHOES",
        "description": "These premium adidas shoes are a nod to the Golden Age of basketball. Step into history reimagined for today with a suede and full grain leather upper, gold foil details and a classic cupsole. Whether courtside or in everyday life, these kicks keep you comfortably connected to the game.",
        "price": 259.99,
        "units_available": 230,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/6de71e6a8ca5465aa3703c8aac8a0bab_9366/Forum_84_Low_CL_Shoes_White_IG3769_01_standard.jpg"
    },
    {
        "name": "SL 72 RS SHOES",
        "description": "Pay homage to the adidas archives with these comfortable shoes. A smooth leather upper and synthetic lining feel soft against your foot while an EVA midsole provides lightweight cushioning. The rubber outsole grips the ground to keep you steady on your feet. Simple yet stylish, these sneakers embody the adidas Originals philosophy of classic sport-inspired design that's made for life.",
        "price": 119.99,
        "units_available": 360,
        "image": "https://assets.adidas.com/images/h_2000,f_auto,q_auto,fl_lossy,c_fill,g_auto/e7d955c4f1fa4f179a4e8308ea7ca8fc_9366/SL_72_RS_Shoes_Blue_IG2132_01_standard.jpg"
    },
]

async def create_products():
    async with app.app_context():
        for product in _products:
            if not Product.query.filter(Product.name==product['name']).one_or_none():
                Product.create(**product)
