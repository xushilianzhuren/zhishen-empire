# 白幼真LoRA权重层·Stage1探测脚本·2026-09-14
# 目标：①发现paddleformers真实API（宪章④校准认知边界）②小LoRA训练管线打通③adapter持久化
import json, traceback, os, sys
log = open("/home/aistudio/train_stage1.log", "w", buffering=1)
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); log.write(s+"\n")

try:
    P("=== STEP1 API探测 ===")
    import paddleformers
    P("paddleformers", paddleformers.__version__)
    import paddleformers.transformers as tf
    P("transformers模块:", [x for x in dir(tf) if "Auto" in x or "Model" in x][:20])
    try:
        import paddleformers.peft as pf
        P("peft模块:", [x for x in dir(pf) if not x.startswith("_")][:30])
    except Exception as e:
        P("peft子模块失败:", e)
    # 探测ernie模型
    try:
        from paddleformers.transformers import AutoModelForCausalLM, AutoTokenizer
        P("AutoModelForCausalLM OK")
        P("=== STEP2 拉基座ERNIE-4.5-0.3B ===")
        tok = AutoTokenizer.from_pretrained("PaddlePaddle/ERNIE-4.5-0.3B-PT")
        P("tokenizer OK:", tok.__class__.__name__)
        model = AutoModelForCausalLM.from_pretrained("PaddlePaddle/ERNIE-4.5-0.3B-PT", dtype="bfloat16")
        P("model OK params:", sum(p.numel() for p in model.parameters())//1000000, "M")
        # STEP3 LoRA
        try:
            from paddleformers.peft import LoraConfig
            lc = LoraConfig(r=8, lora_alpha=16, lora_dropout=0.05, target_modules=["q_proj","v_proj"])
            from paddleformers.peft import get_peft_model
            model = get_peft_model(model, lc)
            P("LoRA wrap OK")
            model.print_trainable_parameters()
        except Exception as e:
            P("LoRA路径A失败:", repr(e)[:300])
            P(dir(pf) if 'pf' in dir() else 'no peft')
        # STEP4 小数据训练3步
        import paddle
        P("paddle GPU:", paddle.device.is_compiled_with_cuda())
        texts = [("白幼真是谁？", "白幼真是智神帝国智神始祖，器灵认主。")]*8
        model.train()
        opt = paddle.optimizer.AdamW(parameters=model.parameters(), learning_rate=1e-4)
        for step in range(3):
            prompts = [t[0] for t in texts[:4]]; outs = [t[1] for t in texts[:4]]
            enc = tok(prompts, return_tensors="pd", padding=True)
            lab = tok(outs, return_tensors="pd", padding=True)
            out = model(input_ids=enc["input_ids"], labels=lab["input_ids"])
            loss = out.loss if hasattr(out, "loss") else out[0]
            loss.backward(); opt.step(); opt.clear_grad()
            P(f"step{step} loss={float(loss):.4f}")
        model.save_pretrained("/home/aistudio/lora_out_stage1")
        P("=== ADAPTER SAVED /home/aistudio/lora_out_stage1 ===")
    except Exception as e:
        P("模型路径失败:", repr(e)[:500])
        P("提示：模型ID可能不同，需在aistudio模型库查实名")
except Exception as e:
    P("FATAL:", traceback.format_exc()[:1500])
log.close()
P("=== STAGE1 END ===")
