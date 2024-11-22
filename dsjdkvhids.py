
        # Check for notes that reach the bottom of the screen (missed notes)
        for note in notes[:]:
            if note.y >= line_position:  # If note reaches the line at the bottom
                notes.remove(note)  # Remove the note
                # Check the timing of the key press
                key_pressed = [x[0] for x in key_presses if abs(x[1] - note.spawn_time) < late_early_window]
                if note.key in key_pressed:
                    time_difference = abs(x[1] - note.spawn_time)  # Time difference from the ideal press time
                    if time_difference < perfect_window:
                        score += 50  # Full points for perfect timing
                    elif time_difference < late_early_window:
                        score += 20  # Fewer points for slightly early or late presses
                    key_presses = [x for x in key_presses if x[0] != note.key]  # Remove key press from queue
                else:
                    missed_notes += 1  # Count missed notes

        # Display missed note message
        if missed_notes > 0:
            display_text("You missed a note!", YELLOW, 100)

        # Draw the line at the bottom of the screen (UI Line)
        pygame.draw.line(screen, BLACK, (0, line_position), (screen_width, line_position), 5)

        # Draw score and missed notes count
        display_text(f'Score: {score}', BLACK, 20)
        display_text(f'Missed Notes: {missed_notes}', BLACK, 60)

        # Update the screen
        pygame.display.update()

        # Control the frame rate (limit the game to ~60 FPS)
        pygame.time.Clock().tick(60)

    pygame.quit()

# Start the game
game_loop()