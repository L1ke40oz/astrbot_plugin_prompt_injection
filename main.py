from astrbot.api.event import AstrMessageEvent
from astrbot.api.event.filter import on_llm_request
from astrbot.api.star import Context, Star, register
from astrbot.core.provider.entities import ProviderRequest


@register("prompt_injection", "YourName", "系统提示词注入插件", "1.0.0")
class PromptInjectionPlugin(Star):
    def __init__(self, context: Context, config: dict = None):
        super().__init__(context, config)
        self.config = config or {}

    def _get_system_prompts(self) -> list[str]:
        configured_prompts = self.config.get("system_prompts", [])
        if not isinstance(configured_prompts, list):
            return []

        prompts = []
        for prompt in configured_prompts:
            if not isinstance(prompt, str):
                continue
            normalized_prompt = prompt.strip()
            if normalized_prompt:
                prompts.append(normalized_prompt)
        return prompts

    @on_llm_request()
    async def on_llm_req(self, event: AstrMessageEvent, request: ProviderRequest):
        prompts = self._get_system_prompts()
        if not prompts:
            return

        injected_prompt = "\n\n".join(prompts)
        if request.system_prompt:
            request.system_prompt += f"\n{injected_prompt}"
        else:
            request.system_prompt = injected_prompt
