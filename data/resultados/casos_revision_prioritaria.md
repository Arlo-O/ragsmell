# Casos de revisi?n prioritaria

Estos casos requieren atenci?n del investigador por incertidumbre, contexto arquitect?nico relevante o posible confusi?n entre una integraci?n leg?tima y la regla operacional. No son etiquetas humanas.

## `bojieli/ai-agent-book|AP1|chapter3/user-memory/agent.py|190|34`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: A long memory-instruction block is selected in a branch and used as a prompt-like instruction.
- Evidencia/limitaci?n: It may be a legitimate mode-specific template/constant; the sample context does not show the call site.
- Motivo: Need inspect the full method and prompt ownership.
- Contexto: `185: - Use `delete_memory` to remove outdated or incorrect memories
186: 
187: Keep memories as simple facts or preferences."""
188:         
189:         elif self.config.memory_mode == MemoryMode.ENHANCED_NOTES:
190:             memory_instructions = """## Memory Management:
191: - All user memories are pre-loaded in the context below
192: - Use `add_memory` to store new important information about the user
193: - Use `update_memory` to modify existing memories
194: - Use `delete_memory` to remove outdated or incorrect memories
195: 
196: IMPORTANT: Each note should contain all important factual information and user preferences in a complete, contextual manner.
197: Notes can be full paragraphs that capture the complete context, not just simple key-value pairs.`

## `khoj-ai/khoj|AP1|src/khoj/processor/operator/grounding_agent_uitars.py|247|39`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: GUI-agent instruction text is defined inside an instruction method and varies by environment.
- Evidencia/limitaci?n: This is plausibly a legitimate provider/agent template, not necessarily infiltration.
- Motivo: Need repository conventions and whether prompts are centralized elsewhere.
- Contexto: `242:         Get the instruction for the agent based on the environment type.
243:         """
244:         UITARS_COMPUTER_PREFIX_PROMPT = """
245:         You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task.
246:         """
247:         UITARS_BROWSER_PREFIX_PROMPT = """
248:         You are a GUI agent. You are given a task and a screenshot of the web browser tab you operate. You need to perform the next action to complete the task.
249:         You control a single tab in a Chromium browser. You cannot access the OS, filesystem, the application window or the addressbar.
250:         """
251: 
252:         UITARS_USR_PROMPT_THOUGHT = """
253:         Try fulfill the user instruction to the best of your ability, especially when the instruction is given multiple times. Do not ignore the instruction.
254: `

## `khoj-ai/khoj|AP1|src/khoj/processor/operator/grounding_agent.py|178|39`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: GUI-agent browser instructions are local constants inside an instruction method.
- Evidencia/limitaci?n: They are likely legitimate templates, but the operational rule still matches a prompt hint and control context.
- Motivo: Need inspect prompt factory/adaptor conventions.
- Contexto: `173:         Get the instruction for the agent based on the environment type.
174:         """
175:         UITARS_COMPUTER_PREFIX_PROMPT = """
176:         You are a GUI agent. You are given a task and your action history, with screenshots. You need to perform the next action to complete the task.
177:         """
178:         UITARS_BROWSER_PREFIX_PROMPT = """
179:         You are a GUI agent. You are given a task and a screenshot of the web browser tab you operate. You need to decide the next action to complete the task.
180:         You control a single tab in a Chromium browser. You cannot access the OS, filesystem or the application window.
181:         Always use the `goto` function to navigate to a specific URL. Ctrl+t, Ctrl+w, Ctrl+q, Ctrl+Shift+T, Ctrl+Shift+W are not allowed.
182:         """
183: 
184:         UITARS_USR_COMPUTER_PROMPT_THOUGHT = f"""
185:         Try fulfill the user instruction to the best of your ability, especially when the instruction is given multiple times. Do not ignore the instruction.`

## `HKUDS/LightRAG|AP1|lightrag/llm/zhipu.py|129|24`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: A short default system prompt is assigned conditionally in an LLM backend function.
- Evidencia/limitaci?n: It is a configurable default and may be a legitimate provider integration.
- Motivo: The complete backend abstraction and configuration path require review.
- Contexto: `124:         raise ImportError("Please install zai-sdk before initialize zhipuai backend.")
125: 
126:     messages = []
127: 
128:     if not system_prompt:
129:         system_prompt = "You are a helpful assistant. Note that sensitive words in the content should be replaced with ***"
130: 
131:     # Add system prompt if provided
132:     if system_prompt:
133:         messages.append({"role": "system", "content": system_prompt})
134:     messages.extend(history_messages)
135:     messages.append({"role": "user", "content": prompt})
136: `

## `multimindlab/multimind-sdk|AP3|multimind/gateway/rag_api.py|315|28`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: A RAG gateway selects OpenAI, Anthropic, or HuggingFace based on available keys but uses literal model defaults.
- Evidencia/limitaci?n: Multiple providers and environment-based selection contradict rigid lock-in.
- Motivo: The extent of configurability and factory boundaries needs researcher review.
- Contexto: `310:         if openai_key:
311:             embedding_model_type = "openai"
312:             embedding_model_name = "text-embedding-ada-002"
313:             embedding_dimension = 1536
314:             embedding_api_key = openai_key
315:             current_model = OpenAIModel(model_name="gpt-3.5-turbo", temperature=0.7)
316: 
317:         elif anthropic_key:
318:             embedding_model_type = "openai"  # Use OpenAI for embeddings
319:             embedding_model_name = "text-embedding-ada-002"
320:             embedding_dimension = 1536
321:             embedding_api_key = None  # Will need OpenAI key for embeddings
322:             current_model = ClaudeModel(model_name="claude-3-sonnet-20240229", temperature=0.7)`

## `mlflow/mlflow|AP4|mlflow/langchain/api_request_parallel_processor.py|128|4`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: The method handles both retriever and chain invocation paths, suggesting mixed retrieval/generation responsibilities.
- Evidencia/limitaci?n: The excerpt does not prove both stages are executed in the same call path or that the method is architecturally monolithic.
- Motivo: Control-flow and class responsibilities require review.
- Contexto: `123:         if self.stream:
124:             return try_transform_response_iter_to_chat_format(response)
125:         else:
126:             return try_transform_response_to_chat_format(response)
127: 
128:     def single_call_api(self, callback_handlers: list[BaseCallbackHandler] | None):
129:         from mlflow.langchain._compat import import_base_retriever
130:         from mlflow.langchain.utils.logging import langgraph_types, lc_runnables_types
131: 
132:         BaseRetriever = import_base_retriever()
133: 
134:         if isinstance(self.lc_model, BaseRetriever):
135:             # Retrievers are invoked differently than Chains`

## `BerriAI/litellm|AP5|litellm/router_rust/invoke/shaping.py|283|4`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: A broad exception around capability discovery returns a fail-open fallback.
- Evidencia/limitaci?n: The source comment documents an intentional best-effort policy, which may be legitimate recovery rather than suppression.
- Motivo: Whether the fallback conceals a critical failure requires researcher judgment.
- Contexto: `278:         supported: Final = host.invoke("get_supported_openai_params")(
279:             model=model,
280:             custom_llm_provider=custom_llm_provider,
281:             base_model=_deployment_base_model(deployment, params),
282:         )
283:     except Exception:  # noqa: BLE001  # best-effort filter: an unresolvable provider must not narrow the request
284:         return True
285:     return supported is None or param in supported
286: 
287: 
288: def _deployment_refuses_reasoning_effort(
289:     deployment: Mapping[str, object], group: str, reasoning_effort: object, host: "PythonHost"
290: ) -> bool:`

## `BerriAI/litellm|AP5|litellm/router_rust/steps/precall.py|250|4`

- Propuesta IA: **UNCERTAIN** (MEDIUM)
- Evidencia de apoyo: The capability-filtering handler uses a documented fail-open fallback after a broad exception.
- Evidencia/limitaci?n: The behavior is intentional and observable through logging; it may be valid resilience.
- Motivo: The criticality of the capability result requires researcher review.
- Contexto: `245:         supported: Final = python_host.invoke("get_supported_openai_params")(  # pyright: ignore[reportUnknownMemberType]  # see count_tokens
246:             model=model,
247:             custom_llm_provider=custom_llm_provider,
248:             base_model=base_model if isinstance(base_model, str) else None,
249:         )
250:     except Exception as e:  # noqa: BLE001  # best-effort filter: an unresolvable provider must not narrow the request
251:         verbose_router_logger.debug(
252:             "litellm.router.py::_deployment_supports_param: keeping %s for model=%s. Got - %s", param, group, e
253:         )
254:         return True
255:     return supported is None or param in supported
256: 
257: `

## `multimindlab/multimind-sdk|AP5|multimind/memory/cognitive_scratchpad.py|135|8`

- Propuesta IA: **UNCERTAIN** (LOW)
- Evidencia de apoyo: A broad exception is logged in a scratchpad reasoning path, but the triggering critical call is outside the excerpt.
- Evidencia/limitaci?n: The detector evidence does not establish whether the failed operation is an LLM/vector call or optional bookkeeping.
- Motivo: Full try block and call context require researcher review.
- Contexto: `130: 
131:             # Update item metadata
132:             item["metadata"]["step_count"] = len(steps["steps"])
133:             item["metadata"]["chain_count"] = 1
134: 
135:         except Exception as e:
136:             logger.error(f"Error tracking reasoning steps: {e}")
137: 
138:     async def _analyze_steps(self) -> None:
139:         """Analyze reasoning steps."""
140:         # Group steps by chain
141:         chain_steps = {}
142:         for step in self.reasoning_steps:`

## `multimindlab/multimind-sdk|AP5|multimind/memory/hierarchical.py|862|8`

- Propuesta IA: **UNCERTAIN** (LOW)
- Evidencia de apoyo: A broad exception is logged during hierarchical semantic analysis, but the relevant critical call is not visible in the excerpt.
- Evidencia/limitaci?n: The available context is insufficient to distinguish LLM failure suppression from ordinary state-update handling.
- Motivo: Full try block must be inspected.
- Contexto: `857:             # Update semantic index
858:             for tag in tags:
859:                 if tag not in self.semantic_index:
860:                     self.semantic_index[tag] = set()
861:                 self.semantic_index[tag].add(node_id)
862:         except Exception as e:
863:             logger.error(f"Error updating semantic analysis: {e}")
864: 
865:     async def _track_node_evolution(self, node_id: str) -> None:
866:         """Track the evolution of a node over time."""
867:         node = self.node_map[node_id]
868:         current_state = {
869:             "timestamp": datetime.now().isoformat(),`

## `bojieli/ai-agent-book|AP3|chapter9/browser-use-rpa/browser-use/browser_use/agent/service.py|200|11`

- Propuesta IA: **FP** (HIGH)
- Evidencia de apoyo: The literal is a fallback when a configurable/default LLM cannot be created.
- Evidencia/limitaci?n: The surrounding code first attempts a configured model and explicitly falls back.
- Motivo: Provider flexibility outside this function is not fully known.
- Contexto: `195: 				except (ImportError, ValueError) as e:
196: 					# Use the logger that's already imported at the top of the module
197: 					logger.warning(
198: 						f'Failed to create default LLM "{default_llm_name}": {e}. Falling back to ChatOpenAI(model="gpt-4.1-mini")'
199: 					)
200: 					llm = ChatOpenAI(model='gpt-4.1-mini')
201: 			else:
202: 				# No default LLM specified, use the original default
203: 				llm = ChatOpenAI(model='gpt-4.1-mini')
204: 
205: 		if page_extraction_llm is None:
206: 			page_extraction_llm = llm
207: 		if available_file_paths is None:`

## `run-llama/llama_index|AP3|llama-index-integrations/postprocessor/llama-index-postprocessor-rankgpt-rerank/llama_index/postprocessor/rankgpt_rerank/base.py|59|27`

- Propuesta IA: **FP** (HIGH)
- Evidencia de apoyo: The RankGPT reranker accepts an injected LLM and creates an OpenAI default only when absent.
- Evidencia/limitaci?n: This is a provider-specific adapter with an abstraction point.
- Motivo: No external factory configuration was inspected.
- Contexto: `54:     def _ensure_llm(self) -> None:
55:         if not self.llm:
56:             try:
57:                 from llama_index.llms.openai import OpenAI
58: 
59:                 self.llm = OpenAI(model="gpt-3.5-turbo-16k")
60:             except ImportError:
61:                 raise RuntimeError(
62:                     "OpenAI LLM is not available. Please install `llama-index-llms-openai` "
63:                     "or provide an alternative LLM instance."
64:                 )
65: 
66:     def _postprocess_nodes(`

## `bojieli/ai-agent-book|AP3|chapter9/browser-use-rpa/browser-use/browser_use/agent/service.py|203|10`

- Propuesta IA: **FP** (HIGH)
- Evidencia de apoyo: This duplicates the configurable browser-agent fallback to ChatOpenAI.
- Evidencia/limitaci?n: The code supports a default LLM and fallback behavior rather than rigidly requiring one provider.
- Motivo: The duplicate finding should be reviewed as one logical case.
- Contexto: `198: 						f'Failed to create default LLM "{default_llm_name}": {e}. Falling back to ChatOpenAI(model="gpt-4.1-mini")'
199: 					)
200: 					llm = ChatOpenAI(model='gpt-4.1-mini')
201: 			else:
202: 				# No default LLM specified, use the original default
203: 				llm = ChatOpenAI(model='gpt-4.1-mini')
204: 
205: 		if page_extraction_llm is None:
206: 			page_extraction_llm = llm
207: 		if available_file_paths is None:
208: 			available_file_paths = []
209: 
210: 		# Set timeout based on model name if not explicitly provided`

## `run-llama/llama_index|AP3|llama-index-core/llama_index/core/program/multi_modal_llm_program.py|64|34`

- Propuesta IA: **FP** (HIGH)
- Evidencia de apoyo: A multimodal program injects a supplied model when available and otherwise creates an OpenAI default.
- Evidencia/limitaci?n: The constructor exposes an abstraction and the literal is a default.
- Motivo: No project-wide provider policy was inspected.
- Contexto: `59:             try:
60:                 from llama_index.llms.openai import (
61:                     OpenAIResponses,
62:                 )  # pants: no-infer-dep
63: 
64:                 multi_modal_llm = OpenAIResponses(model="gpt-4.1", temperature=0)
65:             except ImportError as e:
66:                 raise ImportError(
67:                     "`llama-index-llms-openai` package cannot be found. "
68:                     "Please install it by using `pip install `llama-index-llms-openai`"
69:                 )
70:         if prompt is None and prompt_template_str is None:
71:             raise ValueError("Must provide either prompt or prompt_template_str.")`

## `run-llama/llama_index|AP3|llama-index-core/llama_index/core/evaluation/multi_modal/faithfulness.py|99|41`

- Propuesta IA: **FP** (HIGH)
- Evidencia de apoyo: This evaluation class creates an OpenAI multimodal default but accepts an injected model.
- Evidencia/limitaci?n: The abstraction point is explicit and the provider is a default.
- Motivo: No project-wide default policy was inspected.
- Contexto: `94:                 raise ImportError(
95:                     "llama-index-llms-openai is not installed. "
96:                     "Please install it using `pip install llama-index-multi-modal-llms-openai`"
97:                 )
98: 
99:             self._multi_modal_llm: LLM = OpenAIResponses(
100:                 model="gpt-4.1", max_output_tokens=1000
101:             )
102:         else:
103:             self._multi_modal_llm = multi_modal_llm
104: 
105:         self._raise_error = raise_error
106: `

## `run-llama/llama_index|AP3|llama-index-core/llama_index/core/evaluation/multi_modal/relevancy.py|78|41`

- Propuesta IA: **FP** (HIGH)
- Evidencia de apoyo: Same pattern as the previous evaluation case: injected model or OpenAI default.
- Evidencia/limitaci?n: The source provides an abstraction point.
- Motivo: Only local context was assessed.
- Contexto: `73:                 raise ImportError(
74:                     "OpenAIMultiModal is not installed. "
75:                     "Please install it using `pip install llama-index-multi-modal-llms-openai`"
76:                 )
77: 
78:             self._multi_modal_llm: LLM = OpenAIResponses(
79:                 model="gpt-4.1", max_output_tokens=1000
80:             )
81:         else:
82:             self._multi_modal_llm = multi_modal_llm
83: 
84:         self._raise_error = raise_error
85: `

## `run-llama/llama_index|AP3|llama-index-core/llama_index/core/query_engine/multi_modal.py|87|40`

- Propuesta IA: **FP** (HIGH)
- Evidencia de apoyo: The multimodal query engine accepts a supplied model and only creates an OpenAI default otherwise.
- Evidencia/limitaci?n: This is configurable fallback logic.
- Motivo: No external factory configuration was inspected.
- Contexto: `82:             try:
83:                 from llama_index.llms.openai import (
84:                     OpenAIResponses,
85:                 )  # pants: no-infer-dep
86: 
87:                 self._multi_modal_llm = OpenAIResponses(
88:                     model="gpt-4.1", max_output_tokens=1000
89:                 )
90:             except ImportError as e:
91:                 raise ImportError(
92:                     "`llama-index-llms-openai` package cannot be found. "
93:                     "Please install it by using `pip install `llama-index-llms-openai`"
94:                 )`

## `multimindlab/multimind-sdk|AP5|multimind/memory/hybrid.py|554|8`

- Propuesta IA: **TP** (MEDIUM)
- Evidencia de apoyo: Evolution failures are logged and the method returns without propagating or reporting a structured failure.
- Evidencia/limitaci?n: This may conceal incomplete memory evolution.
- Motivo: The operation may be intentionally best-effort.
- Contexto: `549:                 }
550:             )
551: 
552:             self.last_evolution = datetime.now()
553: 
554:         except Exception as e:
555:             logger.error(f"Error evolving memories: {e}")
556: 
557:     async def _create_backup(self) -> None:
558:         """Create backup of memory state."""
559:         try:
560:             backup = {
561:                 "timestamp": datetime.now().isoformat(),`

## `multimindlab/multimind-sdk|AP5|multimind/memory/temporal.py|216|8`

- Propuesta IA: **TP** (MEDIUM)
- Evidencia de apoyo: Temporal analysis failures are logged without propagation, allowing the event processing to continue.
- Evidencia/limitaci?n: The analysis result can be missing without an explicit failure signal.
- Motivo: The analysis may be optional enrichment.
- Contexto: `211:             event["metadata"]["temporal_type"] = analysis.get("temporal_type")
212:             event["metadata"]["importance"] = analysis.get("importance", 0.0)
213:             event["metadata"]["recurrence"] = analysis.get("recurrence")
214:             event["metadata"]["analysis_results"] = analysis
215: 
216:         except Exception as e:
217:             logger.error(f"Error analyzing temporal info: {e}")
218: 
219:     async def _find_relationships(self, event_id: str) -> None:
220:         """Find temporal relationships between events."""
221:         event = next(e for e in self.events if e["id"] == event_id)
222: 
223:         for other_event in self.events:`

## `multimindlab/multimind-sdk|AP5|multimind/memory/working.py|279|12`

- Propuesta IA: **TP** (MEDIUM)
- Evidencia de apoyo: Embedding failures are caught and logged while the loop continues, potentially leaving an item without its embedding.
- Evidencia/limitaci?n: This suppresses a critical data-processing failure without propagation.
- Motivo: The enclosing method may have later consistency checks not visible here.
- Contexto: `274: 
275:                     # Update embedding
276:                     idx = self.items.index(item)
277:                     self.item_embeddings[idx] = await self.llm.embeddings(response)
278: 
279:             except Exception as e:
280:                 logger.error(f"Error compressing item: {e}")
281: 
282:     async def _create_backup(self) -> None:
283:         """Create a backup of the current state."""
284:         backup = {
285:             "timestamp": datetime.now().isoformat(),
286:             "items": self.items,`

