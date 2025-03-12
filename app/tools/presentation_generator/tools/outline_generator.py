from pydantic import BaseModel, Field
# from pydantic.v1 import BaseModel, Field
from app.services.logger import setup_logger
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from app.services.schemas import PresentationGeneratorInput
from typing import List
from fastapi import HTTPException

logger = setup_logger(__name__)

class SlidesOutlineRequestArgs:
    def __init__(self, outline_generator_args: PresentationGeneratorInput):
        self.grade_level=outline_generator_args.grade_level,
        self.n_slides=outline_generator_args.n_slides,
        self.topic=outline_generator_args.topic
    
    def to_dict(self) -> dict:
        return {
            "grade_level": self.grade_level,
            "n_slides": self.n_slides,
            "topic": self.topic
        }


class OutlineGenerator:
    def __init__(self, verbose=False,):
        self.verbose = verbose
        self.model = GoogleGenerativeAI(model="gemini-1.5-pro")
        self.parser = JsonOutputParser(pydantic_object=PresentationOutline)

    
    def compile(self):
        try:
            prompt = PromptTemplate(
                    template=(
                        "You are a very smart Teaching Assistant for the grade level of {grade_level}. You create presentation outlines for the students on the provided topics. Construct neatly formatted outline of {n_slides} slides to explain the topic {topic} where first slide is the title slide with a short description and last slide is the conclusion slide with a short summary\n{format_instructions}"
                    ),
                    input_variables=["grade_level", "n_slides", "topic"],
                    partial_variables={"format_instructions":self.parser.get_format_instructions()},
                )
            chain = prompt | self.model | self.parser
            if self.verbose:
                logger.info("Successfully compiled the outline generation pipeline.")

        except Exception as e:
            logger.error(f"Failed to compile LLM pipeline: {e}")
            raise HTTPException(status_code=500, detail="Failed to compile LLM pipeline.")

        return chain

def generate_outline(request_args: SlidesOutlineRequestArgs, verbose=True):
    try:
        pipeline = OutlineGenerator(verbose=verbose)
        chain = pipeline.compile()
        outline = chain.invoke(request_args.to_dict())
        return(outline)

    except Exception as e:
        logger.error(f"Failed to generate presentation outline: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate syllabus from LLM.")


class Slide(BaseModel):
    title: str = Field(description="The title of the Slide")
    content: str = Field(description="The content of the Slide. It must be the exact pullet points or content that will be in the slide, not simple indications")


class PresentationOutline(BaseModel):
    main_title: str = Field(description="The main title of the Presentation")
    list_slides: List[Slide] = Field(description="The full collection of slides about the Presentation")