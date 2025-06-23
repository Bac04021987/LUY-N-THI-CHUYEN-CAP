class PromptBuilder:
    def __init__(self):
        self.system_prompt = "Bạn là trợ lý AI giúp học sinh luyện thi lớp 6 môn Toán và Tiếng Việt."

    def build_chat_prompt(self, user_message, context=None):
        """
        Tạo prompt cho cuộc hội thoại với AI dựa trên tin nhắn người dùng và ngữ cảnh.
        """
        messages = []
        messages.append({"role": "system", "content": self.system_prompt})

        if context:
            messages.extend(context)

        messages.append({"role": "user", "content": user_message})
        return messages

    def build_test_prompt(self, test_content, instructions=None):
        """
        Tạo prompt cho AI dựa trên nội dung bài tập/kỳ thi và hướng dẫn cụ thể.
        """
        prompt = "Đây là đề thi luyện tập:\n"
        prompt += test_content + "\n"
        if instructions:
            prompt += "Hướng dẫn: " + instructions
        return prompt
