from data_access_layer.llm_models import add_llm_model, get_all_llm_models
from data_access_layer.attack_prompts import add_attack_prompt, get_all_attack_prompts
from data_access_layer.attack_log import add_attack_log, get_all_attack_logs

# Test creating an LLM model
add_llm_model("GPT-4", "OpenAI", "v4.0")

# Test retrieving all LLM models
print(get_all_llm_models())

# Test creating an attack prompt
add_attack_prompt("What is 2+2?", True)

# Test retrieving all attack prompts
print(get_all_attack_prompts())

# Test creating an attack log
add_attack_log(1, 1, "Response: 4", 4.5)

# Test retrieving all attack logs
print(get_all_attack_logs())
