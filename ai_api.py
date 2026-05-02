#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from transformers.utils import logging

# 禁用进度条和警告（全局一次）
logging.disable_progress_bar()
logging.set_verbosity_error()

class AI:
    def __init__(self, model_name="Qwen/Qwen2-0.5B-Instruct"):
        """初始化模型，只加载一次"""
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.dtype = torch.float16 if self.device == "cuda" else torch.float32
        self.max_new_tokens = 200
        self.temperature = 0.7
        self.top_p = 0.9
        self.system_prompt = "你是一个有帮助的助手，用简洁的中文回答。"
        
        print("正在加载模型...")
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            dtype=self.dtype,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True,
        )
        if self.device == "cpu":
            self.model = self.model.to(self.device)
        self.model.eval()
        print("模型加载完成\n")
        
        self.response = ""   # 存储最后一次回复

    def get_response(self, user_question):
        """根据用户问题获取回复，并保存到 self.response"""
        print("正在获取回答...")
        self.response = self._generate(user_question)
        print(f"AI 回复：{self.response}")
        return self.response

    def _generate(self, user_question):
        """内部生成方法，返回回复文本"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_question},
        ]
        text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        input_ids = self.tokenizer.encode(text, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                input_ids,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                do_sample=True,
                pad_token_id=self.tokenizer.pad_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        
        generated_ids = outputs[0]
        new_tokens = generated_ids[input_ids.shape[1]:]
        response = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return response