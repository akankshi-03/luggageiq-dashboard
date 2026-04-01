import pandas as pd
import numpy as np
import random
import json
from datetime import datetime, timedelta

random.seed(42)
np.random.seed(42)

BRANDS = {
    "Safari": {
        "price_range": (2500, 8000),
        "avg_rating": 4.1,
        "discount_range": (15, 35),
        "market_position": "mid-premium",
        "strengths": ["build quality", "wheels", "spacious", "durable material"],
        "weaknesses": ["zipper quality", "weight", "limited colors"],
    },
    "Skybags": {
        "price_range": (1800, 6000),
        "avg_rating": 3.9,
        "discount_range": (20, 45),
        "market_position": "value",
        "strengths": ["stylish design", "lightweight", "affordable", "color variety"],
        "weaknesses": ["durability", "handle issues", "zipper breaks", "poor customer service"],
    },
    "American Tourister": {
        "price_range": (3500, 12000),
        "avg_rating": 4.3,
        "discount_range": (10, 30),
        "market_position": "premium",
        "strengths": ["premium feel", "sturdy build", "smooth wheels", "brand trust", "warranty"],
        "weaknesses": ["expensive", "heavy", "limited budget options"],
    },
    "VIP": {
        "price_range": (1500, 5000),
        "avg_rating": 3.7,
        "discount_range": (25, 50),
        "market_position": "budget",
        "strengths": ["affordable", "lightweight", "wide availability"],
        "weaknesses": ["quality issues", "handle breaks", "zipper problems", "poor finish"],
    },
    "Aristocrat": {
        "price_range": (1200, 4000),
        "avg_rating": 3.5,
        "discount_range": (30, 55),
        "market_position": "budget",
        "strengths": ["very affordable", "lightweight", "basic functionality"],
        "weaknesses": ["poor durability", "cheap plastic", "zipper fails fast", "wobbly wheels"],
    },
    "Nasher Miles": {
        "price_range": (3000, 10000),
        "avg_rating": 4.2,
        "discount_range": (12, 28),
        "market_position": "mid-premium",
        "strengths": ["modern design", "TSA lock", "smooth spinner wheels", "spacious compartments"],
        "weaknesses": ["price", "weight", "availability of service centers"],
    },
}

PRODUCT_TYPES = ["Cabin", "Medium", "Large", "Set of 2", "Set of 3"]
MATERIALS = ["Polycarbonate", "ABS", "Fabric", "Hardside", "Softside"]
COLORS = ["Black", "Navy Blue", "Red", "Grey", "Blue", "Green", "Purple", "Maroon"]

POSITIVE_TEMPLATES = [
    "The {feature} is excellent! Very happy with this purchase.",
    "Really impressed with the {feature}. Worth every rupee.",
    "Great {feature}, exactly what I needed for my travels.",
    "The {feature} works perfectly. Highly recommended!",
    "Superb {feature}! My family loved it.",
    "Amazing {feature} for this price range. Value for money!",
    "{feature} is top notch. Will buy again.",
    "Used it for 3 trips, {feature} still perfect.",
    "Ordered for Goa trip, {feature} exceeded expectations.",
    "Best luggage for the price! {feature} is outstanding.",
]

NEGATIVE_TEMPLATES = [
    "Very disappointed with the {feature}. Broke after first use.",
    "The {feature} is terrible. Do not buy!",
    "Poor quality {feature}. Expected better for this price.",
    "{feature} stopped working within a month. Waste of money.",
    "Regret buying this. {feature} is very bad.",
    "Returned the product. {feature} was defective.",
    "Customer service is bad and {feature} quality is poor.",
    "{feature} broke during my very first trip. Very upset.",
    "Not worth it at all. {feature} quality is disappointing.",
    "Quality has gone down. {feature} is not as advertised.",
]

NEUTRAL_TEMPLATES = [
    "Decent product overall. {feature} is okay.",
    "Average quality. {feature} could be better.",
    "Good for occasional use. {feature} is acceptable.",
    "Not great not terrible. {feature} meets basic needs.",
    "Okay product for the price. {feature} is standard.",
]

def generate_review_text(brand_info, sentiment):
    features = brand_info["strengths"] if sentiment == "positive" else brand_info["weaknesses"]
    feature = random.choice(features)

    if sentiment == "positive":
        template = random.choice(POSITIVE_TEMPLATES)
    elif sentiment == "negative":
        template = random.choice(NEGATIVE_TEMPLATES)
    else:
        template = random.choice(NEUTRAL_TEMPLATES)

    return template.format(feature=feature)

def generate_products():
    products = []
    product_id = 1

    for brand, info in BRANDS.items():
        num_products = random.randint(10, 16)
        for _ in range(num_products):
            ptype = random.choice(PRODUCT_TYPES)
            material = random.choice(MATERIALS)
            color = random.choice(COLORS)

            list_price = random.randint(info["price_range"][0], info["price_range"][1])
            discount_pct = random.randint(info["discount_range"][0], info["discount_range"][1])
            sell_price = int(list_price * (1 - discount_pct / 100))

            rating = round(np.clip(np.random.normal(info["avg_rating"], 0.4), 1, 5), 1)
            review_count = random.randint(50, 3000)

            products.append({
                "product_id": f"PROD{product_id:04d}",
                "brand": brand,
                "product_name": f"{brand} {ptype} {material} {color} Luggage",
                "type": ptype,
                "material": material,
                "color": color,
                "list_price": list_price,
                "sell_price": sell_price,
                "discount_pct": discount_pct,
                "rating": rating,
                "review_count": review_count,
                "market_position": info["market_position"],
            })
            product_id += 1

    return pd.DataFrame(products)

def generate_reviews(products_df):
    reviews = []
    review_id = 1

    for _, product in products_df.iterrows():
        brand = product["brand"]
        brand_info = BRANDS[brand]
        num_reviews = random.randint(50, 120)

        # sentiment distribution based on rating
        if product["rating"] >= 4.2:
            pos_pct, neg_pct, neu_pct = 0.65, 0.15, 0.20
        elif product["rating"] >= 3.8:
            pos_pct, neg_pct, neu_pct = 0.50, 0.25, 0.25
        else:
            pos_pct, neg_pct, neu_pct = 0.35, 0.40, 0.25

        for _ in range(num_reviews):
            rand = random.random()
            if rand < pos_pct:
                sentiment = "positive"
                star = random.choice([4, 5])
            elif rand < pos_pct + neg_pct:
                sentiment = "negative"
                star = random.choice([1, 2])
            else:
                sentiment = "neutral"
                star = 3

            days_ago = random.randint(1, 730)
            review_date = datetime.now() - timedelta(days=days_ago)

            review_text = generate_review_text(brand_info, sentiment)

            aspect_scores = {}
            for aspect in ["wheels", "handle", "zipper", "material", "size", "durability"]:
                if aspect in brand_info["strengths"]:
                    aspect_scores[aspect] = round(random.uniform(3.5, 5.0), 1)
                elif aspect in brand_info["weaknesses"]:
                    aspect_scores[aspect] = round(random.uniform(1.5, 3.2), 1)
                else:
                    aspect_scores[aspect] = round(random.uniform(2.5, 4.0), 1)

            reviews.append({
                "review_id": f"REV{review_id:06d}",
                "product_id": product["product_id"],
                "brand": brand,
                "star_rating": star,
                "sentiment": sentiment,
                "review_text": review_text,
                "review_date": review_date.strftime("%Y-%m-%d"),
                "wheels_score": aspect_scores["wheels"],
                "handle_score": aspect_scores["handle"],
                "zipper_score": aspect_scores["zipper"],
                "material_score": aspect_scores["material"],
                "size_score": aspect_scores["size"],
                "durability_score": aspect_scores["durability"],
            })
            review_id += 1

    return pd.DataFrame(reviews)

def compute_brand_summary(products_df, reviews_df):
    summary = []
    for brand in BRANDS.keys():
        b_products = products_df[products_df["brand"] == brand]
        b_reviews = reviews_df[reviews_df["brand"] == brand]

        total_reviews = len(b_reviews)
        pos = len(b_reviews[b_reviews["sentiment"] == "positive"])
        neg = len(b_reviews[b_reviews["sentiment"] == "negative"])
        sentiment_score = round((pos / total_reviews) * 100, 1) if total_reviews > 0 else 0

        top_pros = BRANDS[brand]["strengths"][:3]
        top_cons = BRANDS[brand]["weaknesses"][:3]

        summary.append({
            "brand": brand,
            "total_products": len(b_products),
            "total_reviews": total_reviews,
            "avg_sell_price": round(b_products["sell_price"].mean(), 0),
            "avg_list_price": round(b_products["list_price"].mean(), 0),
            "avg_discount_pct": round(b_products["discount_pct"].mean(), 1),
            "avg_rating": round(b_products["rating"].mean(), 2),
            "sentiment_score": sentiment_score,
            "positive_reviews": pos,
            "negative_reviews": neg,
            "neutral_reviews": total_reviews - pos - neg,
            "market_position": BRANDS[brand]["market_position"],
            "top_pros": ", ".join(top_pros),
            "top_cons": ", ".join(top_cons),
            "avg_wheels_score": round(b_reviews["wheels_score"].mean(), 2),
            "avg_handle_score": round(b_reviews["handle_score"].mean(), 2),
            "avg_zipper_score": round(b_reviews["zipper_score"].mean(), 2),
            "avg_material_score": round(b_reviews["material_score"].mean(), 2),
            "avg_size_score": round(b_reviews["size_score"].mean(), 2),
            "avg_durability_score": round(b_reviews["durability_score"].mean(), 2),
        })

    return pd.DataFrame(summary)

if __name__ == "__main__":
    print("Generating products...")
    products_df = generate_products()
    print(f"  → {len(products_df)} products generated")

    print("Generating reviews...")
    reviews_df = generate_reviews(products_df)
    print(f"  → {len(reviews_df)} reviews generated")

    print("Computing brand summary...")
    summary_df = compute_brand_summary(products_df, reviews_df)

    products_df.to_csv("data/products.csv", index=False)
    reviews_df.to_csv("data/reviews.csv", index=False)
    summary_df.to_csv("data/brand_summary.csv", index=False)

    print("\n✅ Data generation complete!")
    print(f"   Products: data/products.csv ({len(products_df)} rows)")
    print(f"   Reviews:  data/reviews.csv ({len(reviews_df)} rows)")
    print(f"   Summary:  data/brand_summary.csv ({len(summary_df)} rows)")
    print("\nBrand Overview:")
    print(summary_df[["brand", "total_products", "total_reviews", "avg_sell_price", "avg_rating", "sentiment_score"]].to_string(index=False))
