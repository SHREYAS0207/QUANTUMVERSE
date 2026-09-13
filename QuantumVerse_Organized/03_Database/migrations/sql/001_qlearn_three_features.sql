CREATE TABLE IF NOT EXISTS qlearn_topics(id TEXT PRIMARY KEY,title TEXT NOT NULL,category TEXT,theory TEXT,mathematics TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS qlearn_simulations(id TEXT PRIMARY KEY,topic_id TEXT,title TEXT,status TEXT CHECK(status IN('VERIFIED','EDUCATIONAL','APPROXIMATION','UNVERIFIED')),config_json JSONB,validation_json JSONB,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS qlearn_solver_history(id TEXT PRIMARY KEY,user_id TEXT,original_question TEXT,final_answer TEXT,verification_status TEXT,calculation_json JSONB,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS qlearn_conversations(id TEXT PRIMARY KEY,user_id TEXT,title TEXT,context_json JSONB,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS qlearn_conversation_messages(id TEXT PRIMARY KEY,conversation_id TEXT REFERENCES qlearn_conversations(id),role TEXT,content TEXT,context_json JSONB,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS qlearn_experiments(id TEXT PRIMARY KEY,user_id TEXT,name TEXT,topic TEXT,circuit_json JSONB,parameters_json JSONB,results_json JSONB,notes TEXT,created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
CREATE INDEX IF NOT EXISTS idx_qlearn_topics_title ON qlearn_topics(title);
CREATE INDEX IF NOT EXISTS idx_qlearn_solver_user ON qlearn_solver_history(user_id);
