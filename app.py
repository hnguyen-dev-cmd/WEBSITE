import streamlit as st

import streamlit as st
import requests
from bs4 import BeautifulSoup

# --- THE HUNTER FUNCTION (Built-in) ---
def get_tcg_news():
    url = "https://www.pokebeach.com/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        news_data = []
        # Finding the titles and the links
        for post in soup.find_all('h2', limit=5):
            title = post.text.strip()
            link = post.find('a')['href'] if post.find('a') else "#"
            news_data.append({"title": title, "link": link})
        return news_data
    except:
        return []

def get_book_calendar():
    url = "https://lazybookcollector.com/calendar/2026/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        books = []
        # This site uses a table for their calendar
        rows = soup.find_all('tr')
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                # Column 0 is usually the Date, Column 1 is the Title
                date_val = cells[0].get_text(strip=True)
                title_val = cells[1].get_text(strip=True)
                
                # Skip the header row and empty rows
                if "Date" not in date_val and title_val:
                    books.append({
                        "title": title_val,
                        "date": date_val,
                        "publisher": "Special Edition"
                    })
        
        # If the table scraper fails, we grab the "List" version
        if not books:
            for item in soup.find_all('li'):
                text = item.get_text(strip=True)
                if ":" in text: # Usually 'Date: Title'
                    parts = text.split(":", 1)
                    books.append({"title": parts[1], "date": parts[0], "publisher": "Check Site"})
                    
        return books
    except Exception as e:
        return [{"title": f"Error: {str(e)}", "date": "!", "publisher": "System"}]

# --- THE WEBSITE SETUP ---
st.set_page_config(page_title="Drop Central", layout="wide")

# Sidebar Navigation
with st.sidebar:
    st.title("📂 Navigation")
    choice = st.radio("Go to:", ["Dashboard", "🃏 TCG Drops", "📚 Deluxe Books", "💎 Grail Gallery"])
    st.divider()
    st.success("Scraper Status: Active ✅")

# --- PAGE LOGIC ---

if choice == "Dashboard":
    st.title("🚀 Reseller Overview")
    st.write("Welcome back, Hayden. Here is your quick look.")
    
    # Visual Metric Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("Active Monitors", "12")
    col2.metric("New Drops Today", "3")
    col3.metric("Market Sentiment", "Bullish 📈")
    st.divider()
    st.subheader("🔥 Top TCG News (Quick Glance)")
    with st.spinner("Checking PokeBeach..."):
        quick_news = get_tcg_news()
        for news in quick_news[:3]: # Only show top 3
            st.write(f"• {news['title']}")

elif choice == "🃏 TCG Drops":
    st.title("Trading Card News & Drops")
    
    # Create two columns: one for News, one for Twitter
    col_news, col_twitter = st.columns([2, 1]) 
    
    with col_news:
        st.subheader("📰 Latest Announcements")
        with st.spinner('Fetching PokeBeach...'):
            latest_news = get_tcg_news()
            if latest_news:
                for item in latest_news:
                    with st.container(border=True):
                        st.write(f"**{item['title']}**")
                        st.markdown(f"[Source Link]({item['link']})")
    
    with col_twitter:
        st.subheader("🐦 Live Twitter Alerts")
        st.write("Real-time deals from @PokemonDealsTCG")
        
        # --- THE TWITTER EMBED CODE ---
        # This is the "Magic" snippet that pulls the live feed
        twitter_html = """
        <a class="twitter-timeline" 
           data-height="800" 
           data-theme="dark" 
           href="https://twitter.com/PokemonDealsTCG?ref_src=twsrc%5Etfw">
           Tweets by PokemonDealsTCG
        </a> 
        <script async src="https://platform.twitter.com/widgets.js" charset="utf-8"></script>
        """
        
        # This command tells Streamlit to run that HTML code
        st.components.v1.html(twitter_html, height=800, scrolling=True)

elif choice == "📚 Deluxe Books":
    st.title("📖 Deluxe Books & First Editions")
    st.info("Direct Source: LazyBookCollector (2026)")

    # 1. THE ACTION BUTTONS (The Calendar)
    col_a, col_b = st.columns(2)
    with col_a:
        st.link_button("📅 Open Full 2026 Calendar", "https://lazybookcollector.com/calendar/2026/", use_container_width=True, type="primary")
    with col_b:
        st.link_button("🔍 Search Recent Drops", "https://www.google.com/search?q=site:lazybookcollector.com+2026", use_container_width=True)

    st.divider()

    # 2. THE "SAVE A DROP" FORM
    # This allows you to manually save what you found on the calendar
    st.subheader("📝 Save a New Drop")
    with st.expander("Click to add a book from the calendar"):
        with st.form("save_book_form", clear_on_submit=True):
            book_name = st.text_input("Book Name (e.g. 'Suntup - The Road')")
            book_link = st.text_input("Direct Link (e.g. 'https://suntup.press/...')")
            submit_button = st.form_submit_button("Save to My Drops")
            
            if submit_button and book_name:
                if 'saved_books' not in st.session_state:
                    st.session_state.saved_books = []
                # We save it as a dictionary (a mini-folder of info)
                st.session_state.saved_books.append({"name": book_name, "link": book_link})
                st.success(f"Successfully saved {book_name}!")

    st.divider()

    # 3. YOUR SAVED DROPS (The Visual List)
    st.subheader("📌 Your Personal Hunt List")
    
    if 'saved_books' not in st.session_state or len(st.session_state.saved_books) == 0:
        st.write("No books saved yet. Find one on the calendar and add it above!")
    else:
        for index, book in enumerate(st.session_state.saved_books):
            with st.container(border=True):
                c1, c2, c3 = st.columns([3, 2, 1])
                
                with c1:
                    st.write(f"**{book['name']}**")
                
                with c2:
                    if book['link']:
                        st.link_button("Go to Store", book['link'], use_container_width=True)
                    else:
                        st.write("No link provided")
                
                with c3:
                    # A button to check market value instantly
                    ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={book['name'].replace(' ', '+')}+special+edition&LH_Sold=1"
                    st.link_button("💰 Value", ebay_url, use_container_width=True)
                    
        # Optional: Button to clear the list
        if st.button("Clear All Saved Books"):
            st.session_state.saved_books = []
            st.rerun()

elif choice == "💎 Grail Gallery":
    st.title("💎 The Grail Gallery")
    st.write("High-Value Drops & 'Instant Flips' (Curated List)")

    # Data for your high-value items
    grails = [
        {
            "name": "Curious King: The Blade Itself (Lettered)",
            "status": "Sold Out / Resale Only",
            "value": "£1,800+",
            "image": "https://curiousking.co.uk/wp-content/uploads/2022/05/The-Blade-Itself-Lettered-Edition-1-scaled.jpg",
            "note": "Lettered editions are the 'holy grail' for CK collectors."
        },
        {
            "name": "Suntup: American Gods (Lettered)",
            "status": "Shipping Jan 2026",
            "value": "$3,500+",
            "image": "https://suntup.press/wp-content/uploads/2023/11/American-Gods-Lettered-Edition-1.jpg",
            "note": "Neil Gaiman signed editions have massive 1st edition premiums."
        },
        {
            "name": "Grim Oak: The Wise Man's Fear",
            "status": "Pre-order June 17, 2026",
            "value": "TBA (High Demand)",
            "image": "https://grimoakpress.com/cdn/shop/files/TheNameoftheWind_Limited_Front_720x.jpg",
            "note": "Patrick Rothfuss signed books are 'FCFS' (Fastest Finger First)."
        }
    ]

    # Create the Visual Grid
    cols = st.columns(2)
    for index, item in enumerate(grails):
        with cols[index % 2]:
            with st.container(border=True):
                # Displays the image from the URL
                st.image(item['image'], use_container_width=True)
                st.subheader(item['name'])
                
                c1, c2 = st.columns(2)
                c1.metric("Est. Value", item['value'])
                c2.write(f"**Status:** {item['status']}")
                
                st.write(f"💡 {item['note']}")
                
                # Instant check buttons
                if st.button(f"Track Market for {index}", use_container_width=True):
                    st.toast(f"Adding {item['name']} to your watchlist...")