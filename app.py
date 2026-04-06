import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# --- 1. SYSTEM UTILITIES (Saving Data) ---
WATCHLIST_FILE = "my_watchlist.csv"

def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        return pd.read_csv(WATCHLIST_FILE).to_dict('records')
    return []

def save_to_watchlist(item_name, link, date):
    new_data = pd.DataFrame([{"Item": item_name, "Link": link, "Date": date}])
    if os.path.exists(WATCHLIST_FILE):
        new_data.to_csv(WATCHLIST_FILE, mode='a', header=False, index=False)
    else:
        new_data.to_csv(WATCHLIST_FILE, index=False)

# --- 2. THE HUNTERS (Scrapers) ---
def get_tcg_news():
    url = "https://www.pokebeach.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [{"title": post.text.strip(), "link": post.find('a')['href']} for post in soup.find_all('h2', limit=5)]
    except: return []

def get_shoe_raffles():
    # Placeholder for Sneaktorious Scraper
    return [{"title": "Jordan 4 'Military Blue'", "site": "Nike SNKRS", "type": "Draw"},
            {"title": "Yeezy Boost 350 V2", "site": "Adidas Confirmed", "type": "Raffle"}]

# --- 3. THE WEBSITE SETUP ---
st.set_page_config(page_title="Drop Central", layout="wide")

with st.sidebar:
    st.title("🎓 Resell University")
    st.write("---")
    # Login Placeholder (Simulator)
    st.text_input("User ID", value="Hayden_Pro")
    choice = st.radio("Niches", ["🏠 Dashboard", "🃏 TCG & Cards", "📚 Deluxe Books", "👟 Shoes & Clothes", "🎤 Artists & Merch", "📌 My Watchlist"])
    st.divider()
    st.success("Monitors: Online 🟢")

# --- 4. PAGE LOGIC ---

if choice == "🏠 Dashboard":
    st.title("🚀 Reseller Overview")
    col1, col2, col3 = st.columns(3)
    col1.metric("Hot Drops", "5", "New")
    col2.metric("Raffles Open", "12")
    col3.metric("Market", "Bullish 📈")
    
    st.subheader("🔥 Instant-Flip Grails")
    # Curated High-Value items
    st.warning("⚠️ **One Piece OP-01 Booster Box** (First Release) - High Resale Potential")
    st.info("💎 **Curious King: Lettered Editions** - Target these for max profit")

elif choice == "🃏 TCG & Cards":
    st.title("Trading Card News & Raffles")
    c1, c2 = st.columns([2, 1])
    with c1:
        st.subheader("📰 TCG Announcements")
        for news in get_tcg_news():
            with st.container(border=True):
                st.write(f"**{news['title']}**")
                st.link_button("View Source", news['link'])
    with c2:
        st.subheader("🐦 Live Alerts")
        twitter_html = '<a class="twitter-timeline" data-height="600" data-theme="dark" href="https://twitter.com/PokemonDealsTCG"></a> <script async src="https://platform.twitter.com/widgets.js"></script>'
        st.components.v1.html(twitter_html, height=600)

elif choice == "📚 Deluxe Books":
    st.title("📖 Deluxe Books & First Editions")
    
    # 1. THE HOT TERMINAL: 2026 Past Grails (Market Performance)
    st.subheader("🔥 The Hot Terminal: 2026 Performance")
    st.info("Direct links to eBay Sold proof for the year's biggest releases.")

    # Data based on your high-value 2026 drops
    hot_past_2026 = [
        {"name": "Red Rising (Subterranean Press)", "release": "March 2026", "query": "Red Rising Subterranean Press 2026"},
        {"name": "The Blade Itself (Curious King)", "release": "Jan 2026", "query": "Curious King Blade Itself Lettered"},
        {"name": "American Gods (Suntup Numbered)", "release": "Feb 2026", "query": "Suntup American Gods Numbered"},
        {"name": "The Shining (Suntup)", "release": "Early 2026", "query": "Suntup The Shining Numbered"}
    ]

    cols = st.columns(2)
    for idx, book in enumerate(hot_past_2026):
        with cols[idx % 2]:
            with st.container(border=True):
                st.write(f"### {book['name']}")
                st.write(f"📅 Released: {book['release']}")
                # Direct link to eBay sold listings to avoid bot blocks
                ebay_sold_url = f"https://www.ebay.com/sch/i.html?_nkw={book['query'].replace(' ', '+')}&LH_Sold=1&LH_Complete=1"
                st.link_button("📊 View Live eBay Market Proof", ebay_sold_url, use_container_width=True)

    st.divider()

    # 2. SAVE AN UPCOMING DROP (With Resale Potential)
    st.subheader("📝 Add Upcoming 2026 Drop")
    with st.form("book_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            b_name = st.text_input("Book Name")
            b_press = st.selectbox("Publisher/Press", ["Curious King", "Suntup", "Subterranean", "Grim Oak", "Lit Escalates", "Other"])
        with col2:
            b_edition = st.selectbox("Edition Type", ["Lettered (A-Z)", "Numbered", "Signed/Limited", "Standard"])
            b_date = st.date_input("Drop Date")
        
        b_link = st.text_input("Store Link")
        
        if st.form_submit_button("Save to Sorted Watchlist"):
            # CALCULATE RESALE POTENTIAL (Logic based on Press & Scarcity)
            potential = 5 # Base
            if b_press in ["Curious King", "Suntup", "Lit Escalates"]: potential += 3
            if b_edition == "Lettered (A-Z)": potential += 2
            elif b_edition == "Numbered": potential += 1
            
            save_to_watchlist(f"{b_name} [Potential: {min(potential, 10)}/10]", b_link, str(b_date))
            st.success("Saved and Sorted by Date!")

    st.divider()

    # 3. SORTED WATCHLIST (Earliest First)
    st.subheader("📌 Your Sorted Hunt List")
    items = load_watchlist()
    if items:
        # Sort by Date (Earliest to Latest)
        items.sort(key=lambda x: x['Date'])
        for i in items:
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 1, 1])
                c1.write(f"**{i['Item']}**")
                c2.write(f"📅 {i['Date']}")
                if i['Link'] and i['Link'] != "N/A":
                    c3.link_button("Store", i['Link'], use_container_width=True)
    else:
        st.write("No upcoming drops saved.")

elif choice == "👟 Shoes & Clothes":
    st.title("👟 Footwear & Apparel")
    st.info("Tracking: Nike, Supreme, and Sneaktorious")
    for shoe in get_shoe_raffles():
        with st.container(border=True):
            st.write(f"### {shoe['title']}")
            st.write(f"**Method:** {shoe['type']} | **Site:** {shoe['site']}")
            st.button("Search Market", key=shoe['title'])

elif choice == "🎤 Artists & Merch":
    st.title("🎤 Artist Merch & Signed Drops")
    st.write("Tracking: Taylor Swift, Limited Tour Merch, Signed CDs")
    st.link_button("🛒 Taylor Swift Store", "https://store.taylorswift.com/")
    st.warning("Monitor this page for 'Signed' keyword restocks.")

elif choice == "📌 My Watchlist":
    st.title("📌 Your Personal Hunt List")
    items = load_watchlist()
    if items:
        for i in items:
            with st.container(border=True):
                st.write(f"**{i['Item']}**")
                st.write(f"📅 Drop Date: {i['Date']}")
                st.link_button("Go to Drop", i['Link'])
    else:
        st.write("Your watchlist is empty.")