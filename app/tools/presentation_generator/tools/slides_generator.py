# Imports
from pydantic import BaseModel, Field
from app.services.logger import setup_logger
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_google_genai import GoogleGenerativeAI
from app.services.schemas import SlideGeneratorInput
from typing import List
from fastapi import HTTPException


# Declare Logger
logger = setup_logger(__name__)


# Request Args class
class SlideGeneratorRequestArgs:
    def __init__(self, slide_generator_args: SlideGeneratorInput):
        pass

    def to_dic(self) -> dict:
        # return {
            
        # }
        pass


# Execution Class - SlidesGenerator
class SlidesGenerator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.model = GoogleGenerativeAI(model="gemini-1.5-pro")
        # Call all the parsers
        # self.parser = JsonOutputParser(pydantic_object=PresentationOutline)

    def compile(self):
        try:
            prompt = PromptTemplate(
                template=(
                    ""
                ),
                input_variables=[],
                partial_variables={"format_instructions":self.parser.get_format_instructions()}
            )

            chain = prompt | self.model | self.parser

            if self.verbose:
                logger.info("Successfully compiled the outline generation pipeline.")

        except Exception as e:
            logger.error(f"Failed to compile LLM pipeline: {e}")
            raise HTTPException(status_code=500, detail="Failed to compile LLM pipeline.")

        return chain


# Calling function
def generate_slides(request_args: SlideGeneratorRequestArgs, verbose=True):
    try:
        pipeline = SlidesGenerator(verbose=verbose)
        chain = pipeline.compile()
        slides = chain.invoke(request_args.to_dict())
        return(slides)

    except Exception as e:
        logger.error(f"Failed to generate presentation outline: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate syllabus from LLM.")


# Parsers