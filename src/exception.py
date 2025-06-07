# Custom exception class for handling errors in the project.
# It provides a detailed error message including the file name, line number, and error message.

import sys
from src.logger import logging

# static method
def error_message_details(error, error_details: sys):
    """
    This function returns the error message with the information of the file name, line number, 
    and error message.

    Parameters:
    error (Exception): The exception object
    error_details (sys): The sys module with the error information

    Returns:
    str: The error message with the information of the file name, line number, and error message
    """
    _, _, exc_tb = error_details.exc_info()
    # extracting file name from exception traceback
    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    
    return error_message

  
class AppException(Exception):
    def __init__(self, error_message: Exception, error_details: sys):
        super().__init__(error_message)
        """
        Initializes a CustomException instance with a detailed error message.

        Parameters:
        error_message (str): The error message string.
        error_details (sys): The sys module containing error information.

        This constructor calls the error_message_details function to generate
        a detailed error message, including the file name, line number, and
        error message, and assigns it to the error_message attribute.
        """
        self.error_message= error_message_details(error_message, error_details = error_details)
        
    def __str__(self) -> str:
        """
        This method returns the detailed error message stored in the error_message attribute.
        The error message includes the file name, line number, and error message.

        Returns: str: The detailed error message
        """

        return self.error_message
