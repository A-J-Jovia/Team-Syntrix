import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
import os
import random
import re
from typing import Optional

# Global caches for the LLM model
MISTRAL_TOKENIZER = None
MISTRAL_MODEL = None
MISTRAL_DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

class ToneBasedTextRewriter:
    """Advanced text rewriting engine with multiple tone adaptations"""
    def __init__(self):
        self.vocabulary_maps = {
            "Suspenseful": {
                "said": ["whispered", "murmured", "declared ominously", "breathed"],
                "walked": ["crept", "stalked", "moved stealthily", "prowled"],
                "looked": ["peered", "gazed intently", "scrutinized", "observed carefully"],
                "found": ["discovered", "uncovered", "stumbled upon", "revealed"],
                "big": ["enormous", "massive", "towering", "immense"],
                "small": ["tiny", "minuscule", "barely visible", "microscopic"],
                "dark": ["pitch-black", "shadowy", "ominous", "forbidding"],
                "quiet": ["eerily silent", "deathly quiet", "hushed", "soundless"],
                "started": ["began mysteriously", "commenced ominously", "initiated"],
                "happened": ["unfolded", "materialized", "emerged", "manifested"],
                "problem": ["mystery", "enigma", "dark secret", "hidden truth"],
                "important": ["crucial", "vital", "critical", "pivotal"],
                "quickly": ["swiftly", "in a flash", "instantaneously", "like lightning"]
            },
            "Inspiring": {
                "said": ["proclaimed", "declared with passion", "shared enthusiastically", "announced boldly"],
                "walked": ["strode confidently", "marched forward", "stepped with purpose", "advanced courageously"],
                "looked": ["envisioned", "gazed with hope", "focused intently", "observed with clarity"],
                "found": ["achieved", "accomplished", "realized", "attained"],
                "big": ["magnificent", "extraordinary", "remarkable", "outstanding"],
                "small": ["humble yet significant", "precious", "valuable", "meaningful"],
                "difficult": ["challenging yet rewarding", "growth-inspiring", "character-building"],
                "good": ["exceptional", "remarkable", "outstanding", "extraordinary"],
                "bad": ["challenging", "learning opportunity", "growth catalyst", "stepping stone"],
                "try": ["commit to", "dedicate yourself to", "embrace", "pursue with passion"],
                "work": ["dedicate yourself", "pour your heart into", "commit passionately"],
                "help": ["empower", "uplift", "inspire", "transform"],
                "success": ["triumph", "breakthrough", "achievement", "victory"],
                "change": ["transformation", "evolution", "breakthrough", "metamorphosis"]
            }
        }
        
        self.sentence_enhancers = {
            "Suspenseful": [
                "The air grew thick with mystery.",
                "Something lurked in the shadows.",
                "An eerie silence filled the space.",
                "Time seemed to slow to a crawl.",
                "The darkness held secrets untold."
            ],
            "Inspiring": [
                "This moment sparked infinite possibilities.",
                "Every challenge became a stepping stone to greatness.",
                "The journey toward excellence had begun.",
                "Dreams transformed into unstoppable reality.",
                "Success was no longer a distant hope, but an approaching certainty."
            ],
            "Neutral": [
                "The analysis revealed important insights.",
                "Further examination showed significant results.",
                "The data supported comprehensive conclusions.",
                "Multiple factors contributed to the outcome.",
                "The findings demonstrated clear patterns."
            ]
        }
    
    def transform_vocabulary(self, text: str, tone: str) -> str:
        """Transform vocabulary based on tone"""
        if tone not in self.vocabulary_maps:
            return text
        
        vocab_map = self.vocabulary_maps[tone]
        result = text
        
        for original, replacements in vocab_map.items():
            if original in result:
                replacement = random.choice(replacements)
                pattern = r'\b' + re.escape(original) + r'\b'
                result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
        
        return result
    
    def restructure_for_tone(self, text: str, tone: str) -> str:
        """Restructure sentences based on tone"""
        sentences = [s.strip() for s in re.split(r'[.!?]+', text) if s.strip()]
        
        if tone == "Suspenseful":
            # Add mysterious connectors and dramatic pauses
            connectors = ["suddenly", "without warning", "in that moment", "unexpectedly", "then"]
            enhanced_sentences = []
            
            for i, sentence in enumerate(sentences):
                if i > 0 and random.random() < 0.4:
                    sentence = f"{random.choice(connectors)}, {sentence}"
                
                # Add dramatic pauses occasionally
                if random.random() < 0.3 and len(sentence) > 20:
                    sentence = sentence + "..."
                    
                enhanced_sentences.append(sentence)
                
                # Add atmospheric sentence occasionally
                if random.random() < 0.25:
                    enhanced_sentences.append(random.choice(self.sentence_enhancers["Suspenseful"]))
                    
        elif tone == "Inspiring":
            # Add motivational connectors and uplifting elements
            connectors = ["furthermore", "beyond that", "even more remarkably", "with unwavering determination"]
            enhanced_sentences = []
            
            for i, sentence in enumerate(sentences):
                if i > 0 and random.random() < 0.3:
                    sentence = f"{random.choice(connectors)}, {sentence}"
                
                enhanced_sentences.append(sentence)
                
                # Add inspiring sentence occasionally
                if random.random() < 0.3:
                    enhanced_sentences.append(random.choice(self.sentence_enhancers["Inspiring"]))
                    
        else:  # Neutral
            enhanced_sentences = sentences
            # Add professional connectors occasionally
            if random.random() < 0.2:
                enhanced_sentences.append(random.choice(self.sentence_enhancers["Neutral"]))
        
        return enhanced_sentences
    
    def rewrite_text(self, text: str, tone: str) -> str:
        """Main rewriting function"""
        if not text.strip():
            return ""
        
        # Transform vocabulary
        transformed = self.transform_vocabulary(text, tone)
        
        # Restructure sentences
        sentences = self.restructure_for_tone(transformed, tone)
        
        # Capitalize and join
        capitalized_sentences = []
        for sentence in sentences:
            if sentence:
                sentence = sentence[0].upper() + sentence[1:] if len(sentence) > 1 else sentence.upper()
                capitalized_sentences.append(sentence)
        
        result = '. '.join(capitalized_sentences) + '.'
        
        # Clean up formatting
        result = re.sub(r'\s+', ' ', result).strip()
        result = re.sub(r'\.+', '.', result)  # Fix multiple dots
        result = re.sub(r'\.\s*\.', '.', result)  # Fix dot spacing
        
        return result

# Initialize the rule-based rewriter
rule_based_rewriter = ToneBasedTextRewriter()

def rewrite_with_llm(text: str, tone: str) -> str:
    """LLM-based rewriting function using the Mistral model."""
    global MISTRAL_TOKENIZER, MISTRAL_MODEL
    
    if not text.strip():
        return ""

    try:
        if MISTRAL_TOKENIZER is None:
            print("Loading Mistral model...")
            model_name = "mistralai/Mistral-7B-Instruct-v0.2"
            MISTRAL_TOKENIZER = AutoTokenizer.from_pretrained(model_name)
            MISTRAL_MODEL = AutoModelForCausalLM.from_pretrained(
                model_name,
                torch_dtype=torch.float16,
                load_in_8bit=True,
                token=os.environ.get("HUGGING_FACE_TOKEN")
            )
        
        prompt_template = f"""
            <|system|>
            You are a helpful assistant that rewrites text to a specific tone.
            The user will provide you with a tone and a piece of text.
            You must rewrite the text using descriptive language and without summarizing the original content.
            The tone should be {tone}.
            </s>
            <|user|>
            Rewrite the following text: {text}
            </s>
            <|assistant|>
        """
        
        inputs = MISTRAL_TOKENIZER(prompt_template, return_tensors="pt")
        inputs = {k: v.to(MISTRAL_DEVICE) for k, v in inputs.items()}
        
        with torch.no_grad():
            outputs = MISTRAL_MODEL.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                pad_token_id=MISTRAL_TOKENIZER.eos_token_id
            )
        
        rewritten_text = MISTRAL_TOKENIZER.decode(outputs[0], skip_special_tokens=True)
        response_text = rewritten_text.split("<|assistant|>")[-1].strip()
        
        return response_text

    except Exception as e:
        print(f"Mistral model failed: {e}")
        return "An error occurred during text rewriting. Please try again."

# --- HYBRID REWRITE FUNCTION ---
# This is the function that will be called by app.py
def hybrid_rewrite(text: str, tone: str) -> str:
    """
    Chooses between the rule-based rewriter and the LLM rewriter.
    """
    word_count = len(text.split())
    
    if word_count < 50:
        # Use the rule-based system for short, simple texts
        print("Using rule-based rewriter...")
        return rule_based_rewriter.rewrite_text(text, tone)
    else:
        # Use the LLM for longer, more complex texts
        print("Using LLM rewriter...")
        return rewrite_with_llm(text, tone)