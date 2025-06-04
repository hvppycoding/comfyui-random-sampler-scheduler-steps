import random

class RandomSamplerSchedulerSteps:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "preset_text": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "ddim,ddim_uniform,20\ndpmpp_2m,karras,50\nipndm_v,kl_optimal,40"
                    }
                )
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "INT")
    RETURN_NAMES = ("sampler", "scheduler", "steps")
    FUNCTION = "run"
    CATEGORY = "Custom/Outpaint"

    def run(self, preset_text):
        lines = [line.strip() for line in preset_text.strip().splitlines() if line.strip()]
        if not lines:
            raise ValueError("No valid presets provided.")

        line = random.choice(lines)
        parts = [x.strip() for x in line.split(",")]

        if len(parts) != 3:
            raise ValueError(f"Invalid preset format: {line}")

        sampler, scheduler, steps_str = parts

        try:
            steps = int(steps_str)
        except ValueError:
            raise ValueError(f"Steps must be an integer: {steps_str}")

        return (sampler, scheduler, steps)

NODE_CLASS_MAPPINGS = {
    "RandomSamplerSchedulerSteps": RandomSamplerSchedulerSteps,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomSamplerSchedulerSteps": "🎲 RandomSamplerSchedulerSteps",
}
