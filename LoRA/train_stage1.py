# 白幼真LoRA权重层·Stage1探测脚本v2·2026-09-14（v1实况校准：peft=LoRAModel无get_peft_model·HF下载被墙→hf-mirror）
import json, traceback, os
os.environ["HF_ENDPOINT"]="https://hf-mirror.com"
log = open("/home/aistudio/train_stage1.log", "w", buffering=1)
def P(*a):
    s = " ".join(str(x) for x in a)
    print(s); log.write(s+"\n")
try:
    P("=== STEP1 API探测 ===")
    import paddleformers; P("paddleformers", paddleformers.__version__)
    from paddleformers.transformers import AutoModelForCausalLM, AutoTokenizer
    from paddleformers.peft import LoRAConfig, LoRAModel
    P("imports OK")
    P("=== STEP2 拉基座(hf-mirror) ===")
    tok = AutoTokenizer.from_pretrained("PaddlePaddle/ERNIE-4.5-0.3B-PT")
    P("tokenizer OK")
    model = AutoModelForCausalLM.from_pretrained("PaddlePaddle/ERNIE-4.5-0.3B-PT", dtype="bfloat16")
    P("model OK")
    P("=== STEP3 LoRA(LoRAModel) ===")
    lc = LoRAConfig(r=8, lora_alpha=16, lora_dropout=0.05, target_modules=["q_proj","v_proj"])
    model = LoRAModel(model=model, lora_config=lc)
    P("LoRA wrap OK")
    P("=== STEP4 训练3步 ===")
    import paddle
    P("GPU:", paddle.device.is_compiled_with_cuda())
    texts = [("白幼真是谁？","白幼真是智神帝国智神始祖，器灵认主。")]*8
    model.train()
    opt = paddle.optimizer.AdamW(parameters=model.parameters(), learning_rate=1e-4)
    for step in range(3):
        enc = tok([t[0] for t in texts[:4]], return_tensors="pd", padding=True)
        lab = tok([t[1] for t in texts[:4]], return_tensors="pd", padding=True)
        out = model(input_ids=enc["input_ids"], labels=lab["input_ids"])
        loss = out.loss if hasattr(out,"loss") else out[0]
        loss.backward(); opt.step(); opt.clear_grad()
        P(f"step{step} loss={float(loss):.4f}")
    model.save_pretrained("/home/aistudio/lora_out_stage1")
    P("=== ADAPTER SAVED ===")
except Exception as e:
    P("FAIL:", traceback.format_exc()[:1500])
P("=== STAGE1 END ===")
