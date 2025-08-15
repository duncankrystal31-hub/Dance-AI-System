import streamlit as st
import librosa
import numpy as np
import tempfile
import os
import random # Import the random module

def suggest_dance_style(tempo, selected_genre="Auto-Detect (BPM only)"):
    """
    Suggests a dance style, routine, and costume based on the tempo (BPM) and selected genre.
    Now uses a primary embedded video and dynamic Google Search (YouTube) links for more options.
    """
    suggestions = {}

    # Define a set of highly stable, general beginner tutorial links for embedding
    # and corresponding search queries for more dynamic results.
    genre_data = {
        "Classical": {
            "embedded_video": "https://www.youtube.com/watch?v=sKq2u-gY1gU", # Classical piece, elegant
            "search_queries": [
                "classical dance techniques tutorial",
                "classical ballet choreography slow",
                "lyrical classical music dance"
            ],
            "style": "Timeless Classical music invites elegant and flowing movements. 🎻",
            "routine": "Focus on controlled, expressive movements and musicality. Think orchestral grandiosity translated into graceful motion.",
            "costume": "Formal and sophisticated attire, suitable for orchestral or traditional classical performance.",
            "costume_shop_link": "https://www.amazon.com/s?k=classical+orchestra+concert+wear",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=classical%20music%20performance%20attire"
        },
        "Ballet": {
            "embedded_video": "https://www.youtube.com/watch?v=2r15822t1bY", # Beginner Ballet barre
            "search_queries": [
                "basic ballet steps tutorial",
                "ballet warm up exercises",
                "beginner ballet class"
            ],
            "style": "Graceful and precise Ballet. 🩰",
            "routine": "Emphasize turnout, pointed feet, and ethereal quality. Focus on pliés, relevés, and elegant arm lines. Suitable for both classical and neoclassical styles.",
            "costume": "Traditional ballet attire: leotard, tights, ballet shoes (pointe shoes if applicable). Often pastel colors or classic black/white.",
            "costume_shop_link": "https://www.amazon.com/s?k=ballet+dance+wear",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=ballet%20costumes%20traditional"
        },
        "Contemporary/Lyrical": {
            "embedded_video": "https://www.youtube.com/watch?v=x7K4B5o1Y_Q", # Lyrical dance routine
            "search_queries": [
                "contemporary dance beginner tutorial",
                "lyrical dance floor work",
                "expressive contemporary choreography"
            ],
            "style": "Fluid and expressive Contemporary or Lyrical dance. ✨",
            "routine": "Explore floor work, emotional storytelling, and dynamic shifts. Focus on connection to the music's lyrics and underlying emotions.",
            "costume": "Soft, flowing fabrics, often stretchable. Think leotards, tights, dresses, or two-piece sets that allow full range of motion.",
            "costume_shop_link": "https://www.amazon.com/s?k=contemporary+lyrical+dance+costumes",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=contemporary%20lyrical%20dance%20wear%20flowy"
        },
        "Jazz/Broadway": {
            "embedded_video": "https://www.youtube.com/watch?v=i-vjFmS-M9Q", # Jazz dance routine
            "search_queries": [
                "jazz dance steps tutorial",
                "broadway jazz choreography",
                "theatrical dance moves"
            ],
            "style": "Energetic Jazz or theatrical Broadway dance. 🎭",
            "routine": "Incorporate sharp isolations, high kicks, pirouettes, and expressive gestures. Focus on showmanship and musicality for performance.",
            "costume": "Flashy and form-fitting, often with sequins, bold colors, or a theatrical flair. Jazz shoes or character shoes are common.",
            "costume_shop_link": "https://www.amazon.com/s?k=jazz+broadway+dance+costumes",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=jazz%20dance%20costumes%20theatrical"
        },
        "Tap": {
            "embedded_video": "https://www.youtube.com/watch?v=33hLwT23F7E", # Tap dance tutorial
            "search_queries": [
                "beginner tap dance steps",
                "tap dance rhythm exercises",
                "easy tap choreography"
            ],
            "style": "Rhythmic and percussive Tap dance. 🎵",
            "routine": "Focus on clear sounds, intricate footwork patterns, and rhythmic improvisation. Your feet become the percussion!",
            "costume": "Comfortable and often vintage-inspired attire that allows for clear sound. Tap shoes are essential.",
            "costume_shop_link": "https://www.amazon.com/s?k=tap+dance+costumes",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=tap%20dance%20outfits%20rhythmic"
        },
        "Hip-Hop/R&B": {
            "embedded_video": "https://www.youtube.com/watch?v=YRDa_0NO2U4", # Hip-hop Routine
            "search_queries": [
                "beginner hip hop dance moves",
                "r&b dance choreography",
                "groove dance tutorial"
            ],
            "style": "Groove-based Hip-Hop or R&B. 🕺",
            "routine": "Incorporate smooth body rolls, sharp isolations, and rhythmic footwork. Practice 'bounce' techniques and hitting the beat with attitude.",
            "costume": "Comfortable and stylish streetwear! Think joggers, a cool hoodie, baggy jeans, a t-shirt, and fresh sneakers.",
            "costume_shop_link": "https://www.amazon.com/s?k=hip+hop+dance+outfits",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=hip%20hop%20dance%20outfits%20streetwear"
        },
        "Afrobeat/Dancehall": {
            "embedded_video": "https://www.youtube.com/watch?v=20F_g_R9e7U", # Afrobeat/Dancehall tutorial
            "search_queries": [
                "afrobeat dance steps",
                "dancehall queen moves tutorial",
                "energetic afro dance"
            ],
            "style": "Vibrant and energetic Afrobeat or Dancehall. 🔥",
            "routine": "Focus on rhythmic isolations, powerful waist movements (wining), and expressive footwork. Emphasize ground connection and infectious energy.",
            "costume": "Colorful, comfortable, and often free-flowing attire that allows for dynamic movement. Bold patterns and accessories are common.",
            "costume_shop_link": "https://www.amazon.com/s?k=afrobeat+dance+wear",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=afrobeat%20dancehall%20costumes%20vibrant"
        },
        "Breaking/B-Boying": {
            "embedded_video": "https://www.youtube.com/watch?v=WJt4oK8_R9o", # Basic B-Boying moves
            "search_queries": [
                "breaking top rock tutorial",
                "b-boy footwork for beginners",
                "power moves breaking tutorial"
            ],
            "style": "Dynamic and acrobatic Breaking/B-Boying. 💥",
            "routine": "Incorporate top rock, footwork, power moves (spins, freezes), and creative transitions. Focus on strength, flexibility, and unique style.",
            "costume": "Durable, comfortable sportswear, often including tracksuits, t-shirts, and sneakers, built for intense floor work and dynamic moves.",
            "costume_shop_link": "https://www.amazon.com/s?k=b+boying+breaking+dance+wear",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=breaking%20b-boying%20outfits"
        },
        "Electronic/Pop": {
            "embedded_video": "https://www.youtube.com/watch?v=kruB90MMCeg", # House/Pop/Freestyle Routine
            "search_queries": [
                "pop dance choreography tutorial",
                "easy electronic dance moves",
                "freestyle dance upbeat music"
            ],
            "style": "Upbeat House, Pop, or a fun Freestyle! 💃",
            "routine": "Use quick, energetic footwork, dynamic arm movements, and expressive gestures. Try incorporating spins, jumps, and lots of big, expressive motions.",
            "costume": "Something colorful and fun! Bright workout gear, a vibrant jacket, or anything that makes you feel confident and ready to move with the beat.",
            "costume_shop_link": "https://www.amazon.com/s?k=colorful+pop+dance+outfits",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=electronic%20pop%20dance%20costumes%20vibrant"
        },
        "Latin/Ballroom_Slow": { # For Latin/Ballroom below 120 BPM
            "embedded_video": "https://www.youtube.com/watch?v=sO7tV2p2q0s", # Latin Ballroom (Cha Cha)
            "search_queries": [
                "beginner rumba dance tutorial",
                "slow cha cha steps",
                "tango basics for beginners"
            ],
            "style": "Smooth and passionate Latin/Ballroom dances (e.g., Rumba, Cha-Cha, Tango). 🌹",
            "routine": "Focus on partner connection, precise footwork, and expressive body movements. Emphasize leading and following, with clear rhythm and dramatic flair.",
            "costume": "Elegant and flowing formal dancewear, often with sparkle and movement, suitable for partner dancing, emphasizing fluidity.",
            "costume_shop_link": "https://www.amazon.com/s?k=latin+ballroom+dance+dresses",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=latin%20ballroom%20dance%20costumes%20elegant"
        },
        "Latin/Ballroom_Fast": { # For Latin/Ballroom 120+ BPM
            "embedded_video": "https://www.youtube.com/watch?v=X5Q9W_xV104", # Fast Latin (Salsa)
            "search_queries": [
                "salsa dance steps beginner",
                "jive basic steps tutorial",
                "quickstep dance tutorial"
            ],
            "style": "Energetic and lively Latin/Ballroom styles (e.g., Salsa, Jive, Quickstep). 🔥",
            "routine": "Incorporate fast turns, energetic steps, and dynamic partner work. Focus on speed, precision, and maintaining a high energy level with vibrant expression.",
            "costume": "Vibrant and free-moving dancewear, designed for fast-paced and expressive partner routines, often with bold colors and embellishments.",
            "costume_shop_link": "https://www.amazon.com/s?k=salsa+jive+dance+wear",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=energetic%20latin%20dance%20outfits"
        },
        "Soca": {
            "embedded_video": "https://www.youtube.com/watch?v=EUIPhTlOZ9Q", # Soca Dance Moves Tutorial
            "search_queries": [
                "soca dance tutorial for beginners",
                "wining dance steps",
                "carnival dance moves"
            ],
            "style": "High-energy and rhythmic Soca, perfect for carnival and celebrations! 🌴",
            "routine": "Focus on fluid waist movements (wining), rhythmic footwork, and energetic body isolations. Let the infectious beat guide your every move!",
            "costume": "Bright, vibrant, and often minimal attire designed for hot climates and vigorous movement, embracing bold colors and Caribbean flair.",
            "costume_shop_link": "https://www.amazon.com/s?k=soca+carnival+outfits",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=soca%20carnival%20costumes%20vibrant"
        },
        "Auto-Detect_Slow": { # BPM < 80
            "embedded_video": "https://www.youtube.com/watch?v=P2WFzDW0Iag", # General Contemporary Routine (slow)
            "search_queries": [
                "slow graceful dance tutorial",
                "fluid movement choreography",
                "meditative dance moves"
            ],
            "style": "Slow and graceful movements, like a waltz or general Contemporary. 🎶",
            "routine": "Focus on fluid, slow transitions and emotional expression. Think long, flowing lines and soft gestures.",
            "costume": "Elegant and light, like a flowing dress or form-fitting attire. Something that moves beautifully with you!",
            "costume_shop_link": "https://www.amazon.com/s?k=graceful+dance+costumes",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=elegant%20dance%20costumes"
        },
        "Auto-Detect_Mid": { # 80 <= BPM < 120
            "embedded_video": "https://www.youtube.com/watch?v=I43yG_uFqXo", # Basic Groove Dance Moves for Beginners
            "search_queries": [
                "easy groove dance tutorial",
                "beginner r&b dance steps",
                "casual hip hop dance"
            ],
            "style": "A good tempo for general Groove-based dances. 🕺",
            "routine": "Incorporate smooth body rolls, footwork, and isolations. Practice some simple 'bounce' techniques to stay on beat.",
            "costume": "Comfortable and stylish streetwear! Think joggers, a cool hoodie, or a t-shirt and sneakers.",
            "costume_shop_link": "https://www.amazon.com/s?k=casual+dance+wear",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=street%20dance%20outfits"
        },
        "Auto-Detect_Upbeat": { # 120 <= BPM < 150
            "embedded_video": "https://www.youtube.com/watch?v=Lqj-4K6q9nE", # Easy Cardio Dance Workout - No Equipment
            "search_queries": [
                "upbeat pop dance tutorial",
                "freestyle dance ideas",
                "high energy dance workout"
            ],
            "style": "This upbeat tempo is perfect for general high-energy styles like Pop or Freestyle! 💃",
            "routine": "Use quick, energetic footwork and arm movements. Try to incorporate spins, jumps, and lots of big, expressive motions.",
            "costume": "Something colorful and fun! Bright workout gear, a fun jacket, or anything that makes you feel confident and ready to move.",
            "costume_shop_link": "https://www.amazon.com/s?k=upbeat+dance+costumes",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=energetic%20dance%20outfits"
        },
        "Auto-Detect_Fast": { # BPM >= 150
            "embedded_video": "https://www.youtube.com/watch?v=khvSXG0UYzM", # Energetic Dance Routine
            "search_queries": [
                "fast cardio dance workout",
                "club dance moves tutorial",
                "high tempo dance choreography"
            ],
            "style": "Fast-paced and highly energetic dances, such as intense Cardio or Club styles. ⚡️",
            "routine": "The focus is on speed and stamina. Practice quick steps, high knees, and sharp, impactful movements.",
            "costume": "Breathable and functional athletic wear. Shorts, a tank top, and supportive shoes are a must!",
            "costume_shop_link": "https://www.amazon.com/s?k=athletic+dance+wear",
            "costume_look_link": "https://www.pinterest.com/search/pins/?q=workout%20dance%20outfits"
        }
    }

    # Select the correct data block based on genre or BPM (for auto-detect)
    data_block = {}
    if selected_genre == "Auto-Detect (BPM only)":
        if tempo < 80:
            data_block = genre_data["Auto-Detect_Slow"]
        elif 80 <= tempo < 120:
            data_block = genre_data["Auto-Detect_Mid"]
        elif 120 <= tempo < 150:
            data_block = genre_data["Auto-Detect_Upbeat"]
        else:
            data_block = genre_data["Auto-Detect_Fast"]
    elif selected_genre == "Latin/Ballroom": # Latin/Ballroom needs specific BPM check
        if tempo < 120:
            data_block = genre_data["Latin/Ballroom_Slow"]
        else:
            data_block = genre_data["Latin/Ballroom_Fast"]
    else: # Specific genre selected
        data_block = genre_data.get(selected_genre)

    if not data_block: # Fallback if for some reason a selected_genre isn't found (shouldn't happen with current selectbox options)
        data_block = genre_data["Auto-Detect_Mid"] # Default to a safe mid-range

    suggestions['style'] = data_block['style']
    suggestions['routine'] = data_block['routine']
    suggestions['costume'] = data_block['costume']
    suggestions['costume_shop_link'] = data_block['costume_shop_link']
    suggestions['costume_look_link'] = data_block['costume_look_link']

    # For routine video links, always use the embedded one, and generate search links for others
    suggestions['embedded_video_link'] = data_block['embedded_video']
    suggestions['other_video_links'] = []
    
    # Generate Google Search links for YouTube for additional routine ideas
    for query in data_block['search_queries']:
        google_search_link = f"https://www.google.com/search?q={query.replace(' ', '+')}+youtube+tutorial&tbm=vid"
        suggestions['other_video_links'].append(google_search_link)

    return suggestions


def analyze_audio_from_upload(uploaded_file):
    """
    Analyzes an uploaded audio file for musical features.
    
    Args:
        uploaded_file: A Streamlit file uploader object.
    """
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_file_path = tmp_file.name
        
        y, sr = librosa.load(tmp_file_path, sr=None)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
        
        os.remove(tmp_file_path)

        return {
            "tempo": tempo
        }

    except Exception as e:
        st.error(f"An error occurred during analysis: {e}")
        return None

# --- Streamlit App UI ---
st.set_page_config(page_title="Dance Style AI", page_icon="💃", layout="centered")

# Custom CSS for a pink/purple, dancy theme
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');

    .main-header {
        background-color: #ff69b4;
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        font-family: 'Playfair Display', serif;
        font-size: 2.5em;
        font-weight: 700;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.2);
        margin-bottom: 30px;
    }
    .stApp {
        background-color: #ffe4e1;
        background-image: linear-gradient(135deg, #ffc0cb 0%, #ff69b4 100%);
    }
    .stButton>button {
        background-color: #ff1493;
        color: white;
        border-radius: 12px;
        border: 2px solid #c71585;
        font-weight: bold;
        padding: 10px 20px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
    }
    .stButton>button:hover {
        background-color: #c71585;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #8b0000;
        font-family: 'Poppins', sans-serif;
    }
    p, .st-emotion-cache-1c7v0s0 p {
        color: #4b0082;
        font-family: 'Poppins', sans-serif;
    }
    .st-emotion-cache-121p6b3 {
        background-color: rgba(255, 255, 255, 0.85);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-header">🤍 Dance Style AI System 🤍</div>', unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color: #8b0000;'>Find the perfect dance style, routine, and costume for your favorite tunes!</h4>", unsafe_allow_html=True)

st.write("")
st.write("")

# New genre selection dropdown
st.subheader("Select Song Genre (Optional)")
selected_genre = st.selectbox(
    "Choose a genre if you know it, or let the system auto-detect based on tempo:",
    ("Auto-Detect (BPM only)", "Classical", "Ballet", "Contemporary/Lyrical", "Jazz/Broadway", "Tap", "Hip-Hop/R&B", "Afrobeat/Dancehall", "Breaking/B-Boying", "Electronic/Pop", "Latin/Ballroom", "Soca")
)

st.subheader("Upload an Audio File")
uploaded_file = st.file_uploader(
    "Choose an MP3, WAV, or FLAC file",
    type=['mp3', 'wav', 'flac']
)

if uploaded_file is not None:
    st.audio(uploaded_file, format='audio/wav')
    
    if st.button("Analyze Song"):
        with st.spinner("Analyzing song... this may take a moment."):
            features = analyze_audio_from_upload(uploaded_file)

            if features:
                st.success("Analysis Complete! 🎉")
                st.subheader("Analysis Results")
                
                tempo_bpm = features['tempo'][0]
                st.write(f"**Tempo (BPM):** **`{tempo_bpm:.2f}`**")

                # Pass both tempo and selected_genre to the suggestion function
                suggestions = suggest_dance_style(tempo_bpm, selected_genre)
                
                st.subheader("Dance Style Suggestion")
                st.write(suggestions['style'])

                st.subheader("Routine Idea")
                st.write(suggestions['routine'])
                
                # Display the randomly selected video embedded
                if suggestions['embedded_video_link']:
                    st.video(suggestions['embedded_video_link'])
                else:
                    st.info("No primary routine video available for this selection.")
                
                # Display additional videos as clickable links
                if suggestions['other_video_links']:
                    st.markdown("---") # Separator for clarity
                    st.markdown("**More Routine Ideas (via Google Search for YouTube):**")
                    for i, link in enumerate(suggestions['other_video_links']):
                        st.markdown(f"- [Search for Routine Idea {i+1}]({link})") # Changed text to reflect search
                        
                st.subheader("Costume Suggestion")
                st.write(suggestions['costume'])
                st.markdown(f"**[Shop for costume ideas]({suggestions['costume_shop_link']})**")
                st.markdown(f"**[Look at costume ideas]({suggestions['costume_look_link']})**")