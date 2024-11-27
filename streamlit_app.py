# app.py
import streamlit as st
import asyncio
from datetime import datetime
import json
from typing import Dict, List
import time

class Agent:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.status = "disponible"
        self.last_task = None
        self.last_result = None
        
    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "last_task": self.last_task,
            "last_result": self.last_result
        }

class TaskManager:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.tasks: List[Dict] = []
        
    def add_agent(self, name: str, description: str):
        self.agents[name] = Agent(name, description)
        
    def add_task(self, task_description: str, assigned_agent: str):
        task = {
            "description": task_description,
            "agent": assigned_agent,
            "status": "pendiente",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "completed_at": None,
            "result": None
        }
        self.tasks.append(task)
        return task
        
    def process_task(self, task_index: int):
        """Simula el procesamiento de una tarea"""
        task = self.tasks[task_index]
        agent = self.agents[task["agent"]]
        
        # Actualizar estados
        task["status"] = "en proceso"
        agent.status = "ocupado"
        agent.last_task = task["description"]
        
        # Simular procesamiento
        time.sleep(2)
        
        # Completar tarea
        result = f"Tarea completada por {agent.name}: {task['description']}"
        task["status"] = "completado"
        task["completed_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task["result"] = result
        agent.status = "disponible"
        agent.last_result = result
        
        return result

# Inicializar el estado de la aplicación
if 'task_manager' not in st.session_state:
    st.session_state.task_manager = TaskManager()
    # Agregar algunos agentes de ejemplo
    st.session_state.task_manager.add_agent("Agente_1", "Procesa texto")
    st.session_state.task_manager.add_agent("Agente_2", "Analiza imágenes")
    st.session_state.task_manager.add_agent("Agente_3", "Genera respuestas")

def main():
    st.title("🤖 Orquestador de Agentes IA")
    
    # Sidebar para agregar nuevos agentes
    with st.sidebar:
        st.header("Agregar Nuevo Agente")
        new_agent_name = st.text_input("Nombre del Agente")
        new_agent_desc = st.text_area("Descripción")
        if st.button("Agregar Agente"):
            if new_agent_name and new_agent_desc:
                st.session_state.task_manager.add_agent(new_agent_name, new_agent_desc)
                st.success(f"Agente {new_agent_name} agregado exitosamente!")
    
    # Sección principal con pestañas
    tab1, tab2, tab3 = st.tabs(["📝 Nueva Tarea", "👥 Agentes", "📊 Tareas"])
    
    # Pestaña de Nueva Tarea
    with tab1:
        st.header("Crear Nueva Tarea")
        task_description = st.text_area("Descripción de la Tarea")
        available_agents = list(st.session_state.task_manager.agents.keys())
        selected_agent = st.selectbox("Asignar a Agente", available_agents)
        
        if st.button("Crear Tarea"):
            if task_description and selected_agent:
                task = st.session_state.task_manager.add_task(task_description, selected_agent)
                # Procesar la tarea inmediatamente (en un caso real esto sería asíncrono)
                result = st.session_state.task_manager.process_task(len(st.session_state.task_manager.tasks) - 1)
                st.success("¡Tarea creada y procesada exitosamente!")
                st.write("Resultado:", result)
    
    # Pestaña de Agentes
    with tab2:
        st.header("Estado de los Agentes")
        for agent_name, agent in st.session_state.task_manager.agents.items():
            with st.expander(f"{agent_name} - {agent.status}"):
                st.json(agent.to_dict())
    
    # Pestaña de Tareas
    with tab3:
        st.header("Historial de Tareas")
        for task in st.session_state.task_manager.tasks:
            with st.expander(f"Tarea: {task['description'][:50]}..."):
                st.json(task)

if __name__ == "__main__":
    main()
