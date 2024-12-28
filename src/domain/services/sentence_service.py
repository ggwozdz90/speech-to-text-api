from typing import Annotated, List

from fastapi import Depends

from core.logger.logger import Logger
from domain.models.sentence_model import SentenceModel
from domain.models.subtitle_segment_model import SubtitleSegmentModel


class SentenceService:
    def __init__(
        self,
        logger: Annotated[Logger, Depends()],
    ) -> None:
        self.logger = logger

    def create_sentence_models(
        self,
        segments: List["SubtitleSegmentModel"],
    ) -> List[SentenceModel]:
        self.logger.info("Creating sentence models from subtitle segments")

        words_with_counters: List[tuple[str, str]] = []

        for segment in segments:
            words = segment.text.split()
            words_with_counters.extend((word, segment.counter) for word in words)

        sentences = []
        current_sentence = []
        counter_word_counts: dict[str, int] = {}

        for word, counter in words_with_counters:
            current_sentence.append(word)
            counter_word_counts[counter] = counter_word_counts.get(counter, 0) + 1

            if word.endswith(".") or word == words_with_counters[-1][0]:
                total_words = sum(counter_word_counts.values())
                sentence = SentenceModel(
                    text=" ".join(current_sentence),
                    segment_percentage={
                        counter: round(count / total_words, 2) for counter, count in counter_word_counts.items()
                    },
                )
                sentences.append(sentence)
                current_sentence = []
                counter_word_counts = {}

        self.logger.info("Sentence models creation completed")
        return sentences

    def apply_translated_sentences(
        self,
        segments: List[SubtitleSegmentModel],
        translated_sentences: List[SentenceModel],
    ) -> None:
        self.logger.info("Applying translated sentences to subtitle segments")

        sentences_words = {i: sentence.text.split() for i, sentence in enumerate(translated_sentences)}

        for segment in segments:
            segment_text = []

            for i, sentence in enumerate(translated_sentences):
                if segment.counter in sentence.segment_percentage:
                    words = sentences_words[i]
                    total_words = len(sentence.text.split())
                    segment_part = sentence.segment_percentage[segment.counter]
                    word_count = int(round(total_words * segment_part))

                    segment_words = words[:word_count]
                    sentences_words[i] = words[word_count:]

                    if segment_words:
                        segment_text.extend(segment_words)

            segment.text = " ".join(segment_text)

        self.logger.info("Application of translated sentences completed")
