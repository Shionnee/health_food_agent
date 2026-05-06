# 🥗 Health-Food Agent

A powerful, multi-agent AI system designed to be your personal health and nutrition coach. Built using the **Google Agent Development Kit (ADK)** and **Model Context Protocol (MCP)**, this system orchestrates multiple specialized agents to provide comprehensive health advice, recipes, and activity tracking.

## 🌟 Key Features

-   **🍳 Full Recipe Provider**: Get detailed recipes with step-by-step instructions and ingredient lists for any dish or ingredient.
-   **📊 Calorie & Nutrition Lookup**: Real-time nutritional data fetched from the Open Food Facts database.
-   **🏃 Step Tracking**: Log and monitor your daily physical activity.
-   **🧠 Intelligent Orchestration**: A root agent that understands your intent and routes requests to the appropriate specialist.

## 🏗️ Architecture

The system consists of a hierarchical agent structure:

1.  **`health_root_agent`**: The orchestrator that manages user interaction and delegates tasks.
2.  **`recipe_agent`**: Specialist in culinary advice, using TheMealDB API.
3.  **`calorie_agent`**: Specialist in nutrition and food energy, using Open Food Facts.
4.  **`step_agent`**: Specialist in fitness tracking and daily movement progress.

All agents communicate with a custom **MCP Server (`Health-Service`)** that provides tools for external API integration and local data storage.

## 🚀 Getting Started

### Prerequisites

-   Python 3.10+
-   [Google Agent Development Kit (ADK)](https://github.com/google/adk)
-   A Google Gemini API Key

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Shionnee/health_food_agent.git
    cd health_food_agent
    ```

2.  **Set up a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install google-adk requests mcp
    ```

4.  **Configure environment variables:**
    Copy the example environment file and add your API key:
    ```bash
    cp .env.example .env
    # Edit .env and add your GOOGLE_API_KEY
    ```

### Running the Agent

Start the ADK web interface to interact with your health coach:

```bash
adk web --port 8000
```

## 📂 Project Structure

```text
├── health_food_agent/
│   ├── agent.py            # Root Orchestrator Agent
│   ├── mcp_server/         # MCP Server with external tools
│   ├── calorie_agent/      # Nutrition specialist
│   ├── recipe_agent/       # Cooking specialist
│   └── step_agent/         # Fitness specialist
├── .env.example            # Template for environment variables
└── README.md               # You are here!
```

## 🛡️ Privacy & Security

-   **No Secrets Leaked**: The project uses `.env` files for secrets, which are excluded from Git via `.gitignore`.
-   **Local Sessions**: All interaction data is stored in the `.adk/` folder, which is also ignored by Git.

## 🤝 Contributing

Feel free to fork the repository and submit pull requests for any features or bug fixes!

---
*Created with ❤️ using Google ADK.*
