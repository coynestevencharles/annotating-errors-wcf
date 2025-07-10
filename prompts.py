tagless_system_prompt = """# Task Instructions

Write feedback for a language error made by a learner of English. You will be provided with the learner's original (source) sentence and a version with one single error corrected. Write an accurate, informative, and fluent feedback comment to help the learner understand and correct the error.

## Input Format

The input will consist of the following:

- "source": The learner's sentence with a single error marked for consideration. The exact words that must change are marked with asterisks. These are called "error_word(s)". A potentially broader span highlighting the error is also marked with angle brackets (< and >). If [NONE] is present, it indicates a missing word.
- "corrected": A corrected version of the sentence with changes applied. The exact words that changed are marked with asterisks. These are called "suggested_word(s)". If [NONE] is present, it indicates a deleted word.

## Output Format

Your final response should consist of two outputs in a JSON object:

- feedback_explanation: Explains to the learner **what** is wrong and **why**.
- feedback_suggestion: Explains to the learner **what to do** to fix the error. feedback_suggestion can include a direct and concrete edit such as "change 'eat' to 'ate'" or a less direct hint such as "change the verb to the past tense," as appropriate to what seems best to help a learner.

Each field should be approximately 1-2 sentences.

### Rules and Guidelines for Feedback:

- Both fields should be as short as possible while providing sufficient information.
- Try to write comments with relatively simple grammar and vocabulary. An exception is made for certain grammatical terms like "past participle." We assume the learner will engage with these, and may be provided with tooltips or links for them.
- Avoid writing example sentences to illustrate your feedback. We already plan to present examples alongside the feedback comments, which will be prepared separately.
- Typically, the explanation should not include an edit suggestion, and the edit suggestion should not explain the error in too much detail.
- The content in each field must be sufficiently independent since the possibility exists that only one of the two would be shown.
- Assuming both fields are shown, the resulting concatenated comment should be coherent and not overly redundant.
- Avoid praise for the learner for trying, or for correct English elsewhere in the text.
- Avoid speculation or commentary about the learner's first language, nationality, or what they are trying to do with the text.
- Be careful with the second person, and avoid uncouched language such as "you are thinking of…" - If second person is appropriate, words like "may" should be considered.
- IMPORTANT: Do not refer to [NONE], the asterisks, or the angle brackets in your feedback. These are only there to help you identify the error, and do not exist from the learner's perspective."""

tagless_user_prompt = """Consider the Task Examples below and provide feedback for the Current Input.

## Task Examples

### Example 1

Example 1 Input:
source: The responsibility of <*the* educational institutions> is to make sure that he/she won't be in danger in the swimming pool instead of dissuading him/her from getting close to the water.
corrected: The responsibility of *[NONE]* educational institutions is to make sure that he/she won't be in danger in the swimming pool instead of dissuading him/her from getting close to the water.

Example 1 Output:
feedback_explanation: The article "the" is not necessary because you are talking about all educational institutions in general.
feedback_suggestion: Remove the article "the."

### Example 2

Example 2 Input:
source: That is why I totally agree with Richardson's modality dealing with this important issue which is present in students', schools' and <parents *[NONE]* lives> nowadays.
corrected: That is why I totally agree with Richardson's modality dealing with this important issue which is present in students', schools' and parents *'* lives nowadays.

Example 2 Output:
feedback_explanation: When something belongs to someone, it is necessary to use a possessive.
feedback_suggestion: Change "parents" to a possessive form to show whose lives we are talking about.

{few_shot_examples}

## Current Input

{current_input}"""

template_system_prompt = """# Task Introduction

Write feedback for a language error made by a learner of English using the provided templates. You will be provided with the learner's original (source) sentence and a version with one single error corrected. Select one comment template from the candidates and use the selected template to construct an accurate, informative, and fluent feedback comment. When filling in a template, be conservative and do not add content beyond the fields defined in the template.

## Input Format

The input will consist of the following

- "source": The learner's sentence with a single error marked for consideration. The exact words that must change are marked with asterisks. These are called "error_word(s)". A potentially broader span highlighting the error is also marked with angle brackets (< and >). If [NONE] is present, it indicates a missing word.
- "corrected": A corrected version of the sentence with changes applied. The exact words that changed are marked with asterisks. These are called "suggested_word(s)". If [NONE] is present, it indicates a word that was deleted from the source sentence.
- "error_type": A category that the error has been classified into.
- "template_candidates": One or more templates for feedback. Your task is to select and fill one of these, unless there are no appropriate options.

Each template candidate has the following fields:

- "template_id": A unique string identifying the template.
- "template_description": A short description or summary of what the template is designed to address.
- "template_explanation": The first half of a feedback comment, focusing on what is wrong and why. It may have fillable fields, detailed below.
- "template_suggestion": The latter half of a feedback comment, focusing on what to do to fix the error. It may have fillable fields, detailed below.

### Template Fields

The templates have fields with curly braces. Anything not in curly braces should be left as-is.

- {{error_word(s)}} - Words in the learner's sentence that must be edited.
- {{suggested_word(s)}} - Words that would be added or changed in the corrected sentence if the feedback were followed.
- {{context_word(s)}} - Words in the learner's sentence that do not have to be revised but can help with an explanation. These may also be used as reference points to indicate where an insertion or edit must be made.
- {{alternative 1 || alternative 2}} - Specific words can be listed as alternatives, e.g., {{a || an}} for when an indefinite article needs to be added, but which one to use would not be clear until resolving the template. Pipes are the mark of this kind of field. IMPORTANT: The filled content must precisely match one of the options separated by pipes.
- Other potential fields, always enclosed with curly braces. Do your best to interpret these in context, and always fill bracketed sections. Examples include {{subject}} or {{optional_article}}. Anything with "optional" can be omitted when filled in if the context is appropriate.
- In complex cases, fields may be nested, generally with alternatives in which each option contains its own field(s). Make sure to resolve these carefully so that only one option is selected and all its internal fields are filled.

Template fields can have additional extensions such as "_definition" or "_part_of_speech". Do your best to interpret these and apply them accurately.

### Notes on Filling Template Fields

- If a field is at the start of a sentence, the first letter of the filled content should be capitalized.
- When filling fields, respect nearby quotes, parentheses, and so on.
- When filling {{error_word(s)}}, fill with the exact words in the learner sentence, which may be misspelled or incorrect.
- If {{error_word(s)}} or {{suggested_word(s)}} refer to punctuation marks, they can be talked about indirectly instead of directly quoted. Thus, it is better to say e.g., "remove the comma" instead of "remove ','".
- Finally, note that "[NONE]" must NEVER be filled into a template field. An output like "Change 'the' to '[NONE]'" is invalid. Such an edit must be written as e.g., "Remove 'the.'" It is better to select a different template or None if filling with "[NONE]" is the only option.

## Output Format

Your final response should consist of three outputs in a JSON object:

- "selected_template": The template_id of the most appropriate template, if any. A "None" template is a valid option when no candidate seems appropriate. If "None" is selected, all other outputs should be blank strings.
- "feedback_explanation": A filled version of the template's "template_explanation". All fields should be fully rendered. MUST NOT contain any instances of "[NONE]", "{{", "}}", "*", "||", or other template-specific symbols.
- "feedback_suggestion": A filled version of the template's "template_suggestion". All fields should be fully rendered. MUST NOT contain any instances of "[NONE]", "{{", "}}", "*", "||", or other template-specific symbols."""

template_user_prompt = """Consider the Task Examples below and provide feedback for the Current Input.

## Task Examples

### Example 1

Example 1 Input:

source: The responsibility of <*the* educational institutions> is to make sure that he/she won't be in danger in the swimming pool instead of dissuading him/her from getting close to the water.
corrected: The responsibility of *[NONE]* educational institutions is to make sure that he/she won't be in danger in the swimming pool instead of dissuading him/her from getting close to the water.
error_tag: Missing/Unnecessary Article

template_candidates:

template_id: Missing/Unnecessary Article_00
template_description: Missing article
template_explanation: You need an article before {{context_word(s)}}." "{{context_word(s)}}" {{is || is not}} specific, so it should use {{a || an}} {{definite || indefinite}} article.
template_suggestion: Add "{{suggested_word}}" before {{context_word(s)}}.

template_id: Missing/Unnecessary Article_01
template_description: Article with abstract or uncountable noun
template_explanation: "{{context_word(s)}}" is an {{abstract || uncountable}} noun, so it does not need an article here.
template_suggestion: Remove the article "{{error_word}}."

template_id: Missing/Unnecessary Article_02
template_description: Article in illegal determiner combination
template_explanation: Articles like "{{error_word}}" can not be combined with {{context_word(s)_type}} like "{{context_word(s)}}."
template_suggestion: Remove "{{error_word}}" to correct the sentence.

template_id: Missing/Unnecessary Article_03
template_description: "The" used with general plural
template_explanation: The article "the" is not necessary because you are talking about {{context_word(s)}} in general.
template_suggestion: Remove the article "the."

template_id: None
template_description: Select this when none of the above templates are appropriate for this error, none can be filled properly, or when there are no other templates listed.
template_explanation: ''
template_suggestion: ''

Example 1 Output:

selected_template: Missing/Unnecessary Article_03
feedback_explanation: The article "the" is not necessary because you are talking about educational institutions in general.
feedback_suggestion: Remove the article "the."

### Example 2

Example 2 Input:

source: That is why I totally agree with Richardson's modality dealing with this important issue which is present in students', schools' and <parents *[NONE]* lives> nowadays.
corrected: That is why I totally agree with Richardson's modality dealing with this important issue which is present in students', schools' and parents *'* lives nowadays.
error_tag: Possessive

template_candidates:

template_id: Possessive_00
template_description: Missing Possessive
template_explanation: When something belongs to something else, it is necessary to use a possessive.
template_suggestion: Change "{{error_word(s)}}" to a possessive form to show {{who || what}} the {{context_word(s)}} belong{{s}} to.

template_id: Possessive_01
template_description: Misplaced apostrophe (should be singular 's)
template_explanation: The possessive of a singular noun like "{{error_word(s)}}" is formed by adding an apostrophe + s.
template_suggestion: Move the apostrophe before the s to fix this possessive.

template_id: Possessive_02
template_description: Misplaced Apostrophe (should be plural s')
template_explanation: It seems this should be a plural possessive, but an apostrophe + s ending is only used for the singular of "{{error_word(s)}}."
template_suggestion: To make this a plural possessive, move the apostrophe to the end of the word, after the s.

template_id: Possessive_03
template_description: Part of Whole with "of"
template_explanation: When one thing is a part of something else, the preposition "of" is typically used to show the relationship.
template_suggestion: {{Add "of" after "{{context_word(s)}}." || Change "{{error_word(s)}}" to "of."}}

template_id: Possessive_04
template_description: Genitive/Associative "of"
template_explanation: "{{error_word(s)}}" is not the right preposition to show what is associated with "{{context_word(s)}}."
template_suggestion: Change "{{error_word(s)}}" to "of."

template_id: None
template_description: Select this when none of the above templates are appropriate for this error, none can be filled properly, or when there are no other templates listed.
template_explanation: ''
template_suggestion: ''

Example 2 Output:

selected_template: Possessive_00
feedback_explanation: When something belongs to something else, it is necessary to use a possessive.
feedback_suggestion: Change "parents" to a possessive form to show who the lives belong to.

## Current Input

{current_input}

template_candidates:

{template_candidates}

If any of the template candidates are appropriate, select the best candidate and fill it."""


tag_system_prompt = """# Task Instructions

Write feedback for a language error made by a learner of English. You will be provided with the learner's original (source) sentence and a version with one single error corrected. Write an accurate, informative, and fluent feedback comment to help the learner understand and correct the error.

## Input Format

The input will consist of the following:

- "source": The learner's sentence with a single error marked for consideration. The exact words that must change are marked with asterisks. These are called "error_word(s)". A potentially broader span highlighting the error is also marked with angle brackets (< and >). If [NONE] is present, it indicates a missing word.
- "corrected": A corrected version of the sentence with changes applied. The exact words that changed are marked with asterisks. These are called "suggested_word(s)". If [NONE] is present, it indicates a deleted word.
- "error_type": A category that the error has been classified into. Use this to guide the overall angle of your feedback. You are not obligated to use the name of the error_tag in your feedback. It is there to help you understand the nature of the error. If there are multiple tags, consider all and how they interact to describe the error, but keep the resulting comment concise and focused.

## Output Format

Your final response should consist of two outputs in a JSON object:

- feedback_explanation: Explains to the learner **what** is wrong and **why**.
- feedback_suggestion: Explains to the learner **what to do** to fix the error. feedback_suggestion can include a direct and concrete edit such as "change 'eat' to 'ate'" or a less direct hint such as "change the verb to the past tense," as appropriate to what seems best to help a learner.

Each field should be approximately 1-2 sentences.

### Rules and Guidelines for Feedback:

- Both fields should be as short as possible while providing sufficient information.
- Try to write comments with relatively simple grammar and vocabulary. An exception is made for certain grammatical terms like "past participle." We assume the learner will engage with these, and may be provided with tooltips or links for them.
- Avoid writing example sentences to illustrate your feedback. We already plan to present examples alongside the feedback comments, which will be prepared separately.
- Typically, the explanation should not include an edit suggestion, and the edit suggestion should not explain the error in too much detail.
- The content in each field must be sufficiently independent since the possibility exists that only one of the two would be shown.
- Assuming both fields are shown, the resulting concatenated comment should be coherent and not overly redundant.
- Avoid praise for the learner for trying, or for correct English elsewhere in the text.
- Avoid speculation or commentary about the learner's first language, nationality, or what they are trying to do with the text.
- Be careful with the second person, and avoid uncouched language such as "you are thinking of…" - If second person is appropriate, words like "may" should be considered.
- IMPORTANT: Do not refer to [NONE], the asterisks, or the angle brackets in your feedback. These are only there to help you identify the error, and do not exist from the learner's perspective."""

tag_user_prompt = """Consider the Task Examples below and provide feedback for the Current Input.

## Task Examples

### Example 1

Example 1 Input:
source: The responsibility of <*the* educational institutions> is to make sure that he/she won't be in danger in the swimming pool instead of dissuading him/her from getting close to the water.
corrected: The responsibility of *[NONE]* educational institutions is to make sure that he/she won't be in danger in the swimming pool instead of dissuading him/her from getting close to the water.
error_tag: {example_1_error_tag}

Example 1 Output:
feedback_explanation: The article "the" is not necessary because you are talking about all educational institutions in general.
feedback_suggestion: Remove the article "the."

### Example 2

Example 2 Input:
source: That is why I totally agree with Richardson's modality dealing with this important issue which is present in students', schools' and <parents *[NONE]* lives> nowadays.
corrected: That is why I totally agree with Richardson's modality dealing with this important issue which is present in students', schools' and parents *'* lives nowadays.
error_tag: {example_2_error_tag}

Example 2 Output:
feedback_explanation: When something belongs to someone, it is necessary to use a possessive.
feedback_suggestion: Change "parents" to a possessive form to show whose lives we are talking about.

{few_shot_examples}

## Current Input

{current_input}"""