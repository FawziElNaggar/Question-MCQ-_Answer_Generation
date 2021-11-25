
echo "Get NLTK Files"
python -c "import nltk;nltk.download('punkt');nltk.download('stopwords');nltk.download('wordnet');nltk.download('popular');nltk.download('averaged_perceptron_tagger')"

echo "Download T5 Models"
git clone https://huggingface.co/ramsrigouthamg/t5_squad_v1 build_question/t5_squad_v1

mkdir build_distractor/pre_models
echo "Download Roberta Models"
wget https://github.com/voidful/BDG/releases/download/v2.0/BDG.pt -P build_distractor/pre_models
wget https://github.com/voidful/BDG/releases/download/v2.0/BDG_ANPM.pt -P build_distractor/pre_models
wget https://github.com/voidful/BDG/releases/download/v2.0/BDG_PM.pt -P build_distractor/pre_models
git clone https://huggingface.co/LIAMF-USP/roberta-large-finetuned-race  build_distractor/roberta-large-finetuned-race