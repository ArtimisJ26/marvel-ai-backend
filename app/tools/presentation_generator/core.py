from app.utils.document_loaders import get_docs
from app.tools.presentation_generator.tools.outline_generator import SlidesOutlineRequestArgs, generate_outline
from app.services.logger import setup_logger
from app.api.error_utilities import LoaderError, ToolExecutorError
from app.services.schemas import PresentationGeneratorInput

logger = setup_logger()

def executor(grade_level: str,
             n_slides: int,
             topic: str,
             verbose=False):

    try:
        slide_outline_model = PresentationGeneratorInput(
            grade_level=grade_level,
            n_slides=n_slides,
            topic=topic
        )

        presentation_generator_args = SlidesOutlineRequestArgs(
            slide_outline_model
        )

        outline = generate_outline(presentation_generator_args, verbose=verbose)

        logger.info(f"Presentation generated successfully")

    except LoaderError as e:
        error_message = e
        logger.error(f"Error in Presentation Generator Pipeline -> {error_message}")
        raise ToolExecutorError(error_message)

    except Exception as e:
        error_message = f"Error in executor: {e}"
        logger.error(error_message)
        raise ValueError(error_message)

    return outline