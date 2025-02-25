import random
from discord.ext import commands, tasks
from pato_utils import constants

class TriviaGame:
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.players = {}  # Armazena a pontuação dos jogadores
        self.easy_questions = constants.LOL_TRIVIA_QUESTIONS
        self.hard_questions = constants.LOL_TRIVIA_QUESTIONS_HARD
        self.questions = []  # Lista de perguntas que será usada durante o jogo
        self.current_question = None  # Pergunta atual
        self.current_answer = None  # Resposta para a pergunta atual
        self.is_game_active = False  # Controla se o jogo está ativo
        self.current_question_index = 0  # Índice da pergunta atual
        self.difficulty = None  # Nível de dificuldade escolhido pelo jogador

    async def start_game(self, ctx, difficulty: str):
        """Starts the trivia game with the chosen difficulty."""
        if self.is_game_active:
            await ctx.send("A trivia game is already in progress!")
            return

        # Set difficulty and select 10 random questions
        if difficulty == "easy":
            self.questions = random.sample(list(self.easy_questions.items()), min(10, len(self.easy_questions)))
            self.difficulty = "Easy"
        elif difficulty == "hard":
            self.questions = random.sample(list(self.hard_questions.items()), min(10, len(self.hard_questions)))
            self.difficulty = "Hard"
        else:
            await ctx.send("Please choose a valid difficulty: 'easy' or 'hard'.")
            return

        self.is_game_active = True
        self.players = {}  # Reset player scores
        self.current_question_index = 0  # Reset question index
        await ctx.send(
            f"🎉 The trivia game has started at **{self.difficulty}** difficulty! 10 random questions will be asked. Let's begin!")
        await self.ask_question(ctx)

    async def ask_question(self, ctx):
        """Asks the next question to players."""
        if self.current_question_index >= len(self.questions):
            await self.end_game(ctx)
            return

        question, answer = self.questions[self.current_question_index]
        self.current_question = question
        self.current_answer = answer.lower()
        await ctx.send(f"**Question {self.current_question_index + 1}:** {self.current_question}")

    async def process_answer(self, ctx, answer: str):
        """Processes players' answers and updates scores."""
        if self.current_question is None:
            return

        # Check if the answer is correct
        if answer.lower() == self.current_answer:
            player = ctx.author.name
            if player not in self.players:
                self.players[player] = 0
            self.players[player] += 1
            await ctx.send(f"✅ {player}, your answer is correct! You earned 1 point.")
        else:
            await ctx.send(f"❌ {ctx.author.name}, your answer is incorrect. The correct answer was **{self.current_answer}**.")

        # Move to the next question
        self.current_question_index += 1
        await self.ask_question(ctx)

    async def end_game(self, ctx):
        """Ends the game and announces the winner."""
        self.is_game_active = False
        if not self.players:
            await ctx.send("No winners! The game ended with no correct answers.")
            return

        winner = max(self.players, key=self.players.get)
        score = self.players[winner]
        await ctx.send(f"🏆 The winner is {winner} with {score} points in {self.difficulty} difficulty! 🎉")

    async def stop_game(self, ctx):
        """Stops the trivia game manually."""
        self.is_game_active = False
        await ctx.send("The trivia game has been stopped.")
