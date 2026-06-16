import streamlit as st
import random
import time

# ページの設定
st.set_page_config(page_title="英単語神経衰弱", layout="centered")

st.title("🎴 英単語 神経衰弱ゲーム")
st.write("英語のカードと、その日本語の意味が書かれたカードを揃えてください！")

# セッションステートの初期化
if 'game_started' not in st.session_state:
    st.session_state.game_started = False
    st.session_state.p1_name = "プレイヤー1"
    st.session_state.p2_name = "プレイヤー2"
    st.session_state.p1_attempts = 0
    st.session_state.p2_attempts = 0
    st.session_state.p1_matches = 0
    st.session_state.p2_matches = 0
    st.session_state.turn = 0  # 0: Player1, 1: Player2
    st.session_state.deck = []
    st.session_state.flipped = []
    st.session_state.matched = []

word_pools = {
    "初級": [
        {"en": "Apple", "jp": "りんご"}, {"en": "Cat", "jp": "猫"}, {"en": "Dog", "jp": "犬"},
        {"en": "Water", "jp": "水"}, {"en": "Sun", "jp": "太陽"}, {"en": "Moon", "jp": "月"},
        {"en": "Wind", "jp": "風"}, {"en": "Grape", "jp": "ブドウ"},
    ],
    "中級": [
        {"en": "challenge", "jp": "挑戦"}, {"en": "discover", "jp": "発見する"}, {"en": "believe", "jp": "信じる"},
        {"en": "experience", "jp": "経験"}, {"en": "improve", "jp": "改善する"}, {"en": "healthy", "jp": "健康な"},
        {"en": "knowledge", "jp": "知識"}, {"en": "share", "jp": "共有する"},
    ],
    "上級": [
        {"en": "accurate", "jp": "正確な"}, {"en": "benefit", "jp": "利益"}, {"en": "determine", "jp": "決定する"},
        {"en": "efficient", "jp": "効率的な"}, {"en": "guarantee", "jp": "保証する"}, {"en": "hesitate", "jp": "ためらう"},
        {"en": "maintain", "jp": "維持する"}, {"en": "observe", "jp": "観察する"},
    ]
}

def start_game(p1, p2, diff_level):
    st.session_state.p1_name = p1
    st.session_state.p2_name = p2
    
    # 選択された難易度に応じた単語リスト（全8ペア）を使用
    selected_pairs = word_pools[diff_level]
    
    deck = []
    for i, pair in enumerate(selected_pairs):
        deck.append({"id": i, "text": pair["en"]})
        deck.append({"id": i, "text": pair["jp"]})
    random.shuffle(deck)
    
    st.session_state.deck = deck
    st.session_state.word_pairs = selected_pairs
    st.session_state.game_started = True
    st.session_state.p1_attempts = 0
    st.session_state.p2_attempts = 0
    st.session_state.p1_matches = 0
    st.session_state.p2_matches = 0
    st.session_state.turn = 0
    st.session_state.flipped = []
    st.session_state.matched = []

# --- 設定画面 ---
if not st.session_state.game_started:
    st.header("🎮 ゲーム設定")
    col1, col2 = st.columns(2)
    with col1:
        p1_input = st.text_input("プレイヤー1の名前", value="Player A")
    with col2:
        p2_input = st.text_input("プレイヤー2の名前", value="Player B")
    
    difficulty = st.radio("難易度を選択してください", ["初級", "中級", "上級"], horizontal=True)
    
    if st.button("ゲームスタート！"):
        start_game(p1_input, p2_input, difficulty)
        st.rerun()

# --- ゲーム画面 ---
else:
    current_player_name = st.session_state.p1_name if st.session_state.turn == 0 else st.session_state.p2_name
    
    st.sidebar.header("📊 スコアボード")
    st.sidebar.subheader(st.session_state.p1_name)
    st.sidebar.write(f"試行: {st.session_state.p1_attempts} / 獲得: {st.session_state.p1_matches}")
    st.sidebar.subheader(st.session_state.p2_name)
    st.sidebar.write(f"試行: {st.session_state.p2_attempts} / 獲得: {st.session_state.p2_matches}")
    
    st.sidebar.divider()
    if st.sidebar.button("タイトルに戻る"):
        st.session_state.game_started = False
        st.rerun()

    st.subheader(f"👉 現在の番: **{current_player_name}**")

    # カード表示
    cols_per_row = 4
    num_cards = len(st.session_state.deck)
    for i in range(0, num_cards, cols_per_row):
        cols = st.columns(cols_per_row)
        for j in range(cols_per_row):
            idx = i + j
            if idx < num_cards:
                card = st.session_state.deck[idx]
                with cols[j]:
                    if idx in st.session_state.matched:
                        st.button(card["text"], key=f"matched_{idx}", disabled=True, use_container_width=True)
                    elif idx in st.session_state.flipped:
                        st.button(card["text"], key=f"flipped_{idx}", type="primary", use_container_width=True)
                    else:
                        if st.button("？", key=f"hidden_{idx}", use_container_width=True):
                            if len(st.session_state.flipped) < 2 and idx not in st.session_state.flipped:
                                st.session_state.flipped.append(idx)
                                st.rerun()

    # 判定処理
    if len(st.session_state.flipped) == 2:
        idx1, idx2 = st.session_state.flipped
        card1 = st.session_state.deck[idx1]
        card2 = st.session_state.deck[idx2]
        
        # 試行回数の加算
        if st.session_state.turn == 0:
            st.session_state.p1_attempts += 1
        else:
            st.session_state.p2_attempts += 1
            
        time.sleep(1.0) # カードを見せるための待機

        if card1["id"] == card2["id"]:
            st.session_state.matched.extend([idx1, idx2])
            if st.session_state.turn == 0:
                st.session_state.p1_matches += 1
            else:
                st.session_state.p2_matches += 1
            st.toast("正解！", icon="✅")
        else:
            st.toast("ハズレ！", icon="❌")
        
        st.session_state.flipped = []
        st.rerun()

    # 全クリア判定
    if len(st.session_state.matched) == len(st.session_state.deck):
        if st.session_state.turn == 0:
            st.balloons()
            st.header(f"🎊 {st.session_state.p1_name} 終了！")
            st.write(f"試行回数: {st.session_state.p1_attempts}")
            if st.button(f"次は {st.session_state.p2_name} の番です"):
                # プレイヤー2のために状態をリセット
                st.session_state.turn = 1
                st.session_state.matched = []
                st.session_state.flipped = []
                random.shuffle(st.session_state.deck) # 公平にするため配置をシャッフル
                st.rerun()
        else:
            st.balloons()
            st.header("🎊 全員終了！")
            
            # 勝敗判定（試行回数が少ない方が勝ち）
            s1 = st.session_state.p1_attempts
            s2 = st.session_state.p2_attempts
            
            if s1 < s2:
                winner = st.session_state.p1_name
                result_text = f"{winner} の勝利！ (試行回数: {s1} vs {s2})"
            elif s2 < s1:
                winner = st.session_state.p2_name
                result_text = f"{winner} の勝利！ (試行回数: {s2} vs {s1})"
            else:
                result_text = f"引き分けです！ (試行回数: {s1} vs {s2})"
                
            st.success(result_text)
            if st.button("もう一度遊ぶ"):
                st.session_state.game_started = False
                st.rerun()

st.write("---")
st.caption("ルール：1人ずつ順番に全カードを揃え、最終的に『試行回数が少なかった方』が勝ちとなります。")
