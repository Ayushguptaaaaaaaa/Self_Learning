questions = [
    ["Who is Shah Rukh Khan?", "WWE Wrestler", "Plumber", "Actor", "Astronaut", 3],
    ["What is the capital of France?", "Berlin", "Paris", "Rome", "London", 2],
    ["Which planet is known as the Red Planet?", "Earth", "Venus", "Mars", "Jupiter", 3],
    ["What is the largest mammal?", "Shark", "Blue Whale", "Elephant", "Giraffe", 2],
    ["Who wrote 'Romeo and Juliet'?", "William Shakespeare", "Jane Austen", "Charles Dickens", "Homer", 1],
    ["What is the square root of 64?", "8", "10", "6", "12", 1],
    ["Which country is known as the Land of the Rising Sun?", "India", "South Korea", "Japan", "China", 3],
    ["Who painted the Mona Lisa?", "Claude Monet", "Pablo Picasso", "Leonardo da Vinci", "Vincent van Gogh", 3],
    ["What is the fastest land animal?", "Horse", "Lion", "Cheetah", "Elephant", 3],
    ["Which ocean is the largest?", "Indian Ocean", "Pacific Ocean", "Atlantic Ocean", "Arctic Ocean", 2],
    ["What is the smallest country in the world?", "San Marino", "Vatican City", "Monaco", "Liechtenstein", 2]
]

prizes = [100000, 320000, 400000, 450000,  500000, 1000000, 2000000, 3000000, 4000000, 5000000, 6000000]

prize_pool=0

for i in range(len(questions)):
    print(questions[i][0] + "\n")
    print(f"a. {questions[i][1]}")
    print(f"b. {questions[i][2]}")  
    print(f"c. {questions[i][3]}")
    print(f"d. {questions[i][4]}\n")
    user_answer = int(input("Enter your answer. 1 for a, 2 for b, 3 for c, 4 for d\n"))

    if user_answer == questions[i][5]:
        prize_pool += prizes[i]
        if i == len(questions) - 1:
            print(f"Correct Answer! You have won {prizes[i]} and your total prize pool is now {prize_pool}.")
            print("Congratulations! You are a Millionaire! Game Over.\n")
        else:
            print(f"Correct Answer! You have won {prizes[i]} and your total prize pool is now {prize_pool} Let's Proceed to the next question!\n")
    else:
        print(f"Incorrect Answer! The correct answer was option {questions[i][5]}. Congratulations! You have won a total of {prize_pool}. Better luck next time!\n")
        break

    