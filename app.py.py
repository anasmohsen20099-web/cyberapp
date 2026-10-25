import streamlit as st
import os
from crewai import Agent, Task, Crew, Process
from langchain_groq import ChatGroq

st.set_page_config(page_title="Cyber AI 909", page_icon="🛡️")
st.title("🛡️ Cyber AI - 909 Red Team Assistant")
st.write("أدخل الهدف (موقع، IP، أو يوزرنيم) والذكاء الاصطناعي هيطلعلك خطة الاختراق.")

# قراءة مفتاح Groq من إعدادات السيرفر
api_key = st.secrets["GROQ_API_KEY"] if "GROQ_API_KEY" in st.secrets else os.environ.get("GROQ_API_KEY")

if not api_key:
    st.error("مفتاح GROQ_API_KEY مش موجود في الإعدادات!")
else:
    os.environ["GROQ_API_KEY"] = api_key
    
    target = st.text_input("🎯 الهدف (Target):")
    
    if st.button("توليد خطة الاختراق"):
        if target:
            with st.spinner("جاري تحليل الهدف وتوليد الخطة..."):
                try:
                    llm = ChatGroq(temperature=0.5, model_name="llama3-70b-8192")
                    
                    recon_agent = Agent(
                        role='Red Team Specialist',
                        goal='تحليل الأهداف وعمل خطط اختراق',
                        backstory='أنت خبير أمن سيبراني وبتعرف تجيب معلومات وتحدد الثغرات.',
                        verbose=False,
                        allow_delegation=False,
                        llm=llm
                    )
                    
                    recon_task = Task(
                        description=f'قم بعمل خطة تفصيلية لاختراق {target} في بيئة معملية، واذكر الأدوات.',
                        expected_output='خطة تفصيلية بالخطوات.',
                        agent=recon_agent
                    )
                    
                    my_crew = Crew(
                        agents=[recon_agent],
                        tasks=[recon_task],
                        process=Process.sequential
                    )
                    
                    result = my_crew.kickoff()
                    st.success("تم توليد الخطة بنجاح!")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"حصل إيرور: {e}")
        else:
            st.warning("اكتب اسم الهدف الأول!")
            