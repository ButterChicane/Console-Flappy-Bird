#include <iostream>
#include <thread>
#include <chrono>
#include <conio.h>
#include <cstdlib>

using namespace std;

const int WIDTH = 60;
const int HEIGHT = 30;
const int FRAMERATE = 10;

bool gameover;
int birdX, birdY;
int pipeX, pipeYTop, pipeYBottom;
int score;
int pipeGap = 4;	  // Gap size in the pipe
int pipeSpeed;		  // Determines the pipe speed (higher speed means faster pipes)
int birdGravitySpeed; // Determines how fast gravity pulls the bird down
int birdJumpSpeed;	  // Determines how fast the bird jumps
int gravity = 1;	  // Gravity strength to pull the bird down

// Texture definition
char bird{'@'};
char pipe{'|'};
char wall{'*'};
char ground{'#'};
char air{' '};

enum Direction
{
	Stop = 0,
	Up,
	Down
};
Direction dir;

void setup()
{
	gameover = false;
	dir = Stop;

	// Bird initial position
	birdX = 10;
	birdY = HEIGHT / 2;

	// Pipe initial position
	pipeX = WIDTH - 1;
	pipeYTop = rand() % (HEIGHT - pipeGap);
	pipeYBottom = pipeYTop + pipeGap;

	score = 0;
}

void draw()
{
	system("cls");
	for (int i = 0; i < HEIGHT; i++)
	{
		for (int j = 0; j < WIDTH; j++)
		{
			if (j == birdX && i == birdY)
				cout << bird; // Bird
			else if (j == pipeX && (i < pipeYTop || i > pipeYBottom))
				cout << pipe; // Pipe
			else if (j == 0 || j == WIDTH - 1)
				cout << wall; // Game boundary
			else
				cout << air;
		}
		cout << endl;
	}

	// Draw the ground (bottom boundary)
	for (int i = 0; i < WIDTH; i++)
		cout << ground;

	cout << "\nScore: " << score << endl;
}

void input()
{
	if (_kbhit())
	{
		switch (_getch())
		{
		case 'w': // Press 'w' to make the bird go up
			dir = Up;
			break;
		case 'x': // Press 'x' to quit
			gameover = true;
			break;
		default:
			break;
		}
	}
}

void birdLogic()
{
	// Bird movement
	if (dir == Up)
	{
		birdY -= 1; // Move bird up by 2 rows (can be adjusted for sensitivity)
		dir = Down; // After moving up, set direction back to Down (gravity)
	}
	else if (dir == Down)
	{
		birdY += gravity; // Gravity pulls bird down
	}
}

void pipeLogic()
{
	// Pipe movement
	pipeX--;

	// If the pipe goes out of bounds, reset it and create a new pipe
	if (pipeX < 1)
	{
		pipeX = WIDTH - 1;
		pipeYTop = rand() % (HEIGHT - pipeGap);
		pipeYBottom = pipeYTop + pipeGap;
		score++;
	}
}

void collisionCheck()
{
	// Collision detection
	if (birdY < 0 || birdY >= HEIGHT || (birdX == pipeX && (birdY < pipeYTop || birdY > pipeYBottom)))
	{
		gameover = true;
	}
}

void startCountdown()
{
	cout << "Game starts in 3...\n";
	this_thread::sleep_for(chrono::seconds(1));
	cout << "2...\n";
	this_thread::sleep_for(chrono::seconds(1));
	cout << "1...\n";
	this_thread::sleep_for(chrono::seconds(1));
}

void chooseDifficulty()
{
	char choice;
	cout << "Choose difficulty level: \n";
	cout << "a) Easy (slow) \n";
	cout << "b) Medium \n";
	cout << "c) Hard (fast) \n";
	cout << "Enter your choice (a, b, c): ";
	cin >> choice;

	switch (choice)
	{
	case 'a':
		pipeSpeed = 14;		   // Pipe moves slowly
		birdGravitySpeed = 25; // Bird updates slower
		break;
	case 'b':
		pipeSpeed = 8;		   // Medium pipe speed
		birdGravitySpeed = 15; // Medium bird speed
		break;
	case 'c':
		pipeSpeed = 2.5;	  // Fast pipe speed
		birdGravitySpeed = 9; // Fast bird movement
		break;
	default:
		pipeSpeed = 8;
		birdGravitySpeed = 15;
		break;
	}
}

int main()
{
	srand(time(0)); // Initialize random seed for pipe generation
	setup();
	chooseDifficulty();
	startCountdown();

	int birdUpdateCounter = 0; // To control how often the bird updates
	int pipeUpdateCounter = 0; // To control how often the pipe updates

	while (!gameover)
	{
		draw();
		input();

		// Logic updates at different intervals
		if (pipeUpdateCounter >= pipeSpeed)
		{
			pipeLogic();
			pipeUpdateCounter = 0;
		}
		if (birdUpdateCounter >= birdGravitySpeed)
		{
			birdLogic();
			birdUpdateCounter = 0;
		}

		collisionCheck();

		this_thread::sleep_for(chrono::milliseconds(FRAMERATE)); // Controls game loop speed
		pipeUpdateCounter += FRAMERATE;
		birdUpdateCounter += FRAMERATE;
	}

	cout << "Game Over! Final Score: " << score << endl;

	return 0;
}
