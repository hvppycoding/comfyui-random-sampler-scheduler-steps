import random
import comfy.samplers

class RandomSamplerSchedulerSteps:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "preset_text": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "ddim,ddim_uniform,20\n"
                                   "dpmpp_2m,karras,50\n"
                                   "ipndm_v,kl_optimal,40"
                    }
                ),
                "seed": ("INT", {"default": 0, "min": 0, "max": 4294967295}),
                "mode": (
                    "STRING",
                    {
                        "default": "fixed",
                        "choices": ["fixed", "random", "increment", "decrement"]
                    }
                ),
            }
        }

    RETURN_TYPES = (
        comfy.samplers.KSampler.SAMPLERS,
        comfy.samplers.KSampler.SCHEDULERS,
        "INT",
        "STRING",
        "INT"
    )
    RETURN_NAMES = ("sampler", "scheduler", "steps", "chosen_line", "used_seed")
    FUNCTION = "run"
    CATEGORY = "Custom/Outpaint"

    def run(self, preset_text, seed, mode):
        lines = [line.strip() for line in preset_text.strip().splitlines() if line.strip()]
        if not lines:
            raise ValueError("No valid presets provided.")

        if mode == "random":
            used_seed = random.randint(0, 4294967295)
        elif mode == "increment":
            used_seed = seed + 1
        elif mode == "decrement":
            used_seed = seed - 1 if seed > 0 else 0
        else:  # fixed
            used_seed = seed

        random.seed(used_seed)
        index = random.randint(0, len(lines) - 1)
        line = lines[index]

        parts = [x.strip() for x in line.split(",")]
        if len(parts) != 3:
            raise ValueError(f"Invalid preset format: {line}")

        sampler, scheduler, steps_str = parts
        try:
            steps = int(steps_str)
        except ValueError:
            raise ValueError(f"Steps must be an integer: {steps_str}")

        return (sampler, scheduler, steps, line, used_seed)


NODE_CLASS_MAPPINGS = {
    "RandomSamplerSchedulerSteps": RandomSamplerSchedulerSteps,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomSamplerSchedulerSteps": "🎲 RandomSamplerSchedulerSteps",
}
