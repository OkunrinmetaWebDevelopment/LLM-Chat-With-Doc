import os



# https://python.langchain.com/en/latest/modules/indexes/document_loaders/examples/excel.html?highlight=xlsx#microsoft-excel
from langchain.document_loaders import CSVLoader, PDFMinerLoader, TextLoader, UnstructuredExcelLoader, Docx2txtLoader

# load_dotenv()
ROOT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))

# Define the folder for storing database
SOURCE_DIRECTORY = f"{ROOT_DIRECTORY}/data"

PERSIST_DIRECTORY = f"{ROOT_DIRECTORY}/DB"

DB_FAISS_PATH =f"{ROOT_DIRECTORY}/vectorstore/db_faiss"

MODEL_PATH =f"{ROOT_DIRECTORY}/model"

# # Can be changed to a specific number
# INGEST_THREADS = os.cpu_count() or 8

# Define the Chroma settings


# https://python.langchain.com/en/latest/_modules/langchain/document_loaders/excel.html#UnstructuredExcelLoader
# DOCUMENT_MAP = {
#     ".txt": TextLoader,
#     ".md": TextLoader,
#     ".py": TextLoader,
#     ".pdf": PDFMinerLoader,
#     ".csv": CSVLoader,
#     ".xls": UnstructuredExcelLoader,
#     ".xlsx": UnstructuredExcelLoader,
#     ".docx": Docx2txtLoader,
#     ".doc": Docx2txtLoader,
# }

# Default Instructor Model
EMBEDDING_MODEL_NAME = "hkunlp/instructor-large"
# You can also choose a smaller model, don't forget to change HuggingFaceInstructEmbeddings
# to HuggingFaceEmbeddings in both ingest.py and run_localGPT.py
# EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"


# load the LLM for generating Natural Language responses

# for HF models
# model_id = "TheBloke/vicuna-7B-1.1-HF"
# model_basename = None
# model_id = "TheBloke/Wizard-Vicuna-7B-Uncensored-HF"
# model_id = "TheBloke/guanaco-7B-HF"
# model_id = 'NousResearch/Nous-Hermes-13b' # Requires ~ 23GB VRAM. Using STransformers
# alongside will 100% create OOM on 24GB cards.
# llm = load_model(device_type, model_id=model_id)

# for GPTQ (quantized) models
# model_id = "TheBloke/Nous-Hermes-13B-GPTQ"
# model_basename = "nous-hermes-13b-GPTQ-4bit-128g.no-act.order"
# model_id = "TheBloke/WizardLM-30B-Uncensored-GPTQ"
# model_basename = "WizardLM-30B-Uncensored-GPTQ-4bit.act-order.safetensors" # Requires
# ~21GB VRAM. Using STransformers alongside can potentially create OOM on 24GB cards.
# model_id = "TheBloke/wizardLM-7B-GPTQ"
# model_basename = "wizardLM-7B-GPTQ-4bit.compat.no-act-order.safetensors"
# model_id = "TheBloke/WizardLM-7B-uncensored-GPTQ"
# model_basename = "WizardLM-7B-uncensored-GPTQ-4bit-128g.compat.no-act-order.safetensors"

# for GGML (quantized cpu+gpu+mps) models - check if they support llama.cpp
# model_id = "TheBloke/wizard-vicuna-13B-GGML"
# model_basename = "wizard-vicuna-13B.ggmlv3.q4_0.bin"
# model_basename = "wizard-vicuna-13B.ggmlv3.q6_K.bin"
# model_basename = "wizard-vicuna-13B.ggmlv3.q2_K.bin"
# model_id = "TheBloke/orca_mini_3B-GGML"
# model_basename = "orca-mini-3b.ggmlv3.q4_0.bin"



# # chose device typ to run on as well as to show source documents.
# @click.command()
# @click.option(
#     "--device_type",
#     default="cuda" if torch.cuda.is_available() else "cpu",
#     type=click.Choice(
#         [
#             "cpu",
#             "cuda",
#             "ipu",
#             "xpu",
#             "mkldnn",
#             "opengl",
#             "opencl",
#             "ideep",
#             "hip",
#             "ve",
#             "fpga",
#             "ort",
#             "xla",
#             "lazy",
#             "vulkan",
#             "mps",
#             "meta",
#             "hpu",
#             "mtia",
#         ],
#     ),
#     help="Device to run on. (Default is cuda)",
# )
# @click.option(
#     "--show_sources",
#     "-s",
#     is_flag=True,
#     help="Show sources along with answers (Default is False)",
# )