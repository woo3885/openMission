"""
독립 실행형 GUI 챗봇 애플리케이션
Gemini API와 LangChain을 활용한 ChatGPT 스타일 인터페이스
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# 환경변수 로드
load_dotenv()

class ChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LangChain Chatbot with Gemini")
        self.root.geometry("700x600")
        
        # Gemini API 초기화
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY가 .env 파일에 설정되지 않았습니다.")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-pro",
            google_api_key=api_key,
            temperature=0.7
        )
        
        # 대화 히스토리
        self.chat_history = []
        
        # UI 구성
        self.setup_ui()
        
        # 초기 인사말
        self.display_ai_greeting()
    
    def setup_ui(self):
        """UI 컴포넌트 설정"""
        # 상단 타이틀
        title_frame = tk.Frame(self.root, bg="#343541", height=60)
        title_frame.pack(fill=tk.X)
        title_label = tk.Label(
            title_frame,
            text="🤖 LangChain Gemini Chatbot",
            font=("Arial", 16, "bold"),
            bg="#343541",
            fg="white"
        )
        title_label.pack(pady=15)
        
        # 채팅 영역 (스크롤 가능)
        chat_frame = tk.Frame(self.root, bg="white")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            font=("Arial", 11),
            bg="#f7f7f8",
            fg="#202123",
            state=tk.DISABLED,
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # 텍스트 태그 설정 (AI/User 구분)
        self.chat_display.tag_config("ai", foreground="#10a37f", font=("Arial", 11, "bold"))
        self.chat_display.tag_config("user", foreground="#0084ff", font=("Arial", 11, "bold"))
        
        # 입력 영역
        input_frame = tk.Frame(self.root, bg="white")
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_field = tk.Text(
            input_frame,
            height=3,
            font=("Arial", 11),
            wrap=tk.WORD,
            bg="white",
            fg="#202123",
            relief=tk.SOLID,
            borderwidth=1
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.input_field.bind("<Return>", self.on_enter_key)
        
        # 전송 버튼
        self.send_button = tk.Button(
            input_frame,
            text="전송",
            font=("Arial", 11, "bold"),
            bg="#10a37f",
            fg="white",
            command=self.send_message,
            padx=20,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.send_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # 상태 표시줄
        self.status_label = tk.Label(
            self.root,
            text="준비 완료",
            font=("Arial", 9),
            bg="#f0f0f0",
            fg="#666",
            anchor=tk.W,
            padx=10
        )
        self.status_label.pack(fill=tk.X)
    
    def display_ai_greeting(self):
        """AI 초기 인사말 표시"""
        greeting = "안녕하세요! 저는 Gemini 기반의 AI 어시스턴트입니다. 무엇을 도와드릴까요? 😊"
        self.append_message("AI", greeting)
        self.chat_history.append(AIMessage(content=greeting))
    
    def append_message(self, sender, message):
        """채팅창에 메시지 추가"""
        self.chat_display.config(state=tk.NORMAL)
        
        if sender == "AI":
            self.chat_display.insert(tk.END, "🤖 AI: ", "ai")
        else:
            self.chat_display.insert(tk.END, "👤 You: ", "user")
        
        self.chat_display.insert(tk.END, f"{message}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def on_enter_key(self, event):
        """Enter 키 이벤트 처리 (Shift+Enter는 줄바꿈)"""
        if not event.state & 0x1:  # Shift 키가 눌리지 않았으면
            self.send_message()
            return "break"
    
    def send_message(self):
        """사용자 메시지 전송"""
        user_input = self.input_field.get("1.0", tk.END).strip()
        
        if not user_input:
            return
        
        # 입력창 초기화
        self.input_field.delete("1.0", tk.END)
        
        # 사용자 메시지 표시
        self.append_message("You", user_input)
        self.chat_history.append(HumanMessage(content=user_input))
        
        # 버튼 비활성화 및 상태 업데이트
        self.send_button.config(state=tk.DISABLED)
        self.status_label.config(text="AI가 응답 중...")
        
        # 별도 스레드에서 AI 응답 생성
        threading.Thread(target=self.get_ai_response, daemon=True).start()
    
    def get_ai_response(self):
        """AI 응답 생성 (비동기)"""
        try:
            # Gemini API 호출
            response = self.llm.invoke(self.chat_history)
            ai_message = response.content
            
            # UI 업데이트는 메인 스레드에서 실행
            self.root.after(0, self.display_ai_response, ai_message)
            
        except Exception as e:
            error_msg = f"오류가 발생했습니다: {str(e)}"
            self.root.after(0, self.display_ai_response, error_msg)
    
    def display_ai_response(self, message):
        """AI 응답 표시"""
        self.append_message("AI", message)
        self.chat_history.append(AIMessage(content=message))
        
        # 버튼 활성화 및 상태 업데이트
        self.send_button.config(state=tk.NORMAL)
        self.status_label.config(text="준비 완료")
        self.input_field.focus()

def main():
    """메인 실행 함수"""
    root = tk.Tk()
    app = ChatbotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
