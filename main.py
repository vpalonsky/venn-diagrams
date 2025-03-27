import pygame
import math

WIDTH = 900
HEIGHT = 600
COLUMNS = 180
ROWS = 120
FRAMERATE = 30
BACKGROUND_COLOR = "black"
CIRCLES_BORDER_COLOR = "white"

pygame.init()
surface = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
CIRCLES = [
	{
		"x": WIDTH/2-50,
		"y": HEIGHT/2,
		"r": 60,
		"l": "A",
		"c": "red"
	},
	{
		"x": WIDTH/2+50,
		"y": HEIGHT/2,
		"r": 70,
		"l": "B",
		"c": "lightblue"
	}
]

# class Point():
# 	def __init__(self, x, y):
# 		self.x = x
# 		self.y = y

class Circle():
	def __init__(self, i, x, y, r, l, c):
		self.i = i
		self.x = x
		self.y = y
		self.r = r
		self.l = l
		self.c = c
		# self.points: list[Point] = []
		self.filled = False

def distance_between_points(x1, y1, x2, y2):
	diff_x = x2-x1
	diff_y = y2-y1

	return math.sqrt(math.pow(diff_x, 2) + math.pow(diff_y, 2))

# def classify_points(points: list[list[Point]], circles: list[Circle]):
# 	for row in points:
# 		for point in row:
# 			for circle in circles:
# 				if is_inside_circle(point.x, point.y, circle.x, circle.y, circle.r):
# 					circle.points.append(point)

def draw_circles(surface: pygame.Surface, circles: list[Circle]):
	for circle in circles:
		if circle.filled:
			pygame.draw.circle(surface, circle.c, (circle.x, circle.y), circle.r-1)

		pygame.draw.circle(surface, CIRCLES_BORDER_COLOR, (circle.x, circle.y), circle.r, 1)

		myfont = pygame.font.Font(None, circle.r)
		circle_letter = myfont.render(circle.l, False, CIRCLES_BORDER_COLOR)
		surface.blit(circle_letter, circle_letter.get_rect(center=(circle.x, circle.y)))

def handle_mouse_click(mouse_x, mouse_y, circles: list[Circle]):
	for circle in circles:
		if distance_between_points(mouse_x, mouse_y, circle.x, circle.y) < circle.r:
			circle.filled = not circle.filled

def lines_intersection(vector_a, point_a, vector_b, point_b):
	(vector_a_x, vector_a_y) = vector_a
	(point_a_x, point_a_y) = point_a
	(vector_b_x, vector_b_y) = vector_b
	(point_b_x, point_b_y) = point_b

	slope_a = vector_a_y/vector_a_x
	slope_b = vector_b_y/vector_b_x

	intersection_x = (-point_a_x*slope_a+point_a_y+point_b_x*slope_b-point_b_y)/(slope_b-slope_a)
	intersection_y = (intersection_x-point_b_x)*slope_b+point_b_y

	return (intersection_x, intersection_y)
	# alpha = (point_a_y-point_b_y) / (((vector_a_x+point_a_x-point_b_x)*vector_a_x)/vector_b_x + vector_b_x)

	# return (alpha*vector_a_x+point_a_x, alpha*vector_a_y+point_a_y)

def circles_intersections(circles: list[Circle]):
	for i in range(len(circles)):
		for j in range(i+1, len(circles)):
			(x1, y1, r1) = (circles[i].x, circles[i].y, circles[i].r)
			(x2, y2, r2) = (circles[j].x, circles[j].y, circles[j].r)

			d = distance_between_points(x1, y1, x2, y2)
			if d >= r1+r2 or (x1==x2 and y1==y2): continue

			(rotated_plane_x, rotated_plane_y) = ((x1+x2)/2, (y1+y2)/2)

			(vector_a_x, vector_a_y) = ((x2-x1)/d, (y2-y1)/d)
			(vector_b_x, vector_b_y) = ((y2-y1)/d, -(x2-x1)/d)

			point_a = (r1*r1-r2*r2)/(2*d)
			discriminate = (r1*r1+r2*r2)/2 - math.pow(r1*r1-r2*r2, 2)/(4*d*d) - (d*d)/4
			if discriminate < 0: continue
			point_b1 = math.sqrt(discriminate)
			point_b2 = -math.sqrt(discriminate)

			intersection_x1 = rotated_plane_x + vector_a_x * point_a + vector_b_x * point_b1
			intersection_y1 = rotated_plane_y + vector_a_y * point_a + vector_b_y * point_b1

			intersection_x2 = rotated_plane_x + vector_a_x * point_a + vector_b_x * point_b2
			intersection_y2 = rotated_plane_y + vector_a_y * point_a + vector_b_y * point_b2

			pygame.draw.circle(surface, "white", (intersection_x1, intersection_y1), 5)
			pygame.draw.circle(surface, "white", (intersection_x2, intersection_y2), 5)

			middle_point_x = (intersection_x1+intersection_x2)/2
			middle_point_y = (intersection_y1+intersection_y2)/2

			pygame.draw.circle(surface, "white", (middle_point_x, middle_point_y), 5)

			if intersection_x1!=intersection_x2 and intersection_y1!=intersection_y2:
				vector_principal_x = intersection_x1-middle_point_x
				vector_principal_y = intersection_y1-middle_point_y

				vector_ortogonal_x = vector_principal_y
				vector_ortogonal_y = -vector_principal_x

				slope = vector_ortogonal_y/vector_ortogonal_x

				box_center_dist1 = r1 - distance_between_points(middle_point_x, middle_point_y, x1, y1)
				box_center_dist2 = r2 - distance_between_points(middle_point_x, middle_point_y, x2, y2)

				box_right_x = box_right_y = box_left_x = box_left_y = 0
				if x2>x1:
					box_right_x = box_center_dist1/math.sqrt(1 + slope*slope) + middle_point_x
					box_right_y = (box_center_dist1*slope)/math.sqrt(1 + slope*slope) + middle_point_y
					box_left_x = -box_center_dist2/math.sqrt(1 + slope*slope) + middle_point_x
					box_left_y = -(box_center_dist2*slope)/math.sqrt(1 + slope*slope) + middle_point_y
				else:
					box_right_x = box_center_dist2/math.sqrt(1 + slope*slope) + middle_point_x
					box_right_y = (box_center_dist2*slope)/math.sqrt(1 + slope*slope) + middle_point_y
					box_left_x = -box_center_dist1/math.sqrt(1 + slope*slope) + middle_point_x
					box_left_y = -(box_center_dist1*slope)/math.sqrt(1 + slope*slope) + middle_point_y


				pygame.draw.circle(surface, "white", (box_right_x, box_right_y), 5)
				pygame.draw.circle(surface, "white", (box_left_x, box_left_y), 5)

				(box_up_left_x, box_up_left_y) = lines_intersection((vector_ortogonal_x, vector_ortogonal_y), (intersection_x1, intersection_y1), (vector_principal_x, vector_principal_y), (box_left_x, box_left_y))
				(box_down_left_x, box_down_left_y) = lines_intersection((vector_ortogonal_x, vector_ortogonal_y), (intersection_x2, intersection_y2), (vector_principal_x, vector_principal_y), (box_left_x, box_left_y))
				(box_up_right_x, box_up_right_y) = lines_intersection((vector_ortogonal_x, vector_ortogonal_y), (intersection_x1, intersection_y1), (vector_principal_x, vector_principal_y), (box_right_x, box_right_y))
				(box_down_right_x, box_down_right_y) = lines_intersection((vector_ortogonal_x, vector_ortogonal_y), (intersection_x2, intersection_y2), (vector_principal_x, vector_principal_y), (box_right_x, box_right_y))
				pygame.draw.circle(surface, "white", (box_up_left_x, box_up_left_y), 5)
				pygame.draw.circle(surface, "white", (box_down_left_x, box_down_left_y), 5)
				pygame.draw.circle(surface, "white", (box_up_right_x, box_up_right_y), 5)
				pygame.draw.circle(surface, "white", (box_down_right_x, box_down_right_y), 5)

				actual_point_x = box_down_left_x
				actual_point_y = box_down_left_y
				final_horizontal_point_x = box_down_right_x
				final_horizontal_point_y = box_down_right_y
				final_vertical_point = (box_up_right_x, box_up_right_y)

				# while actual_point_x!=final_vertical_point[0] and actual_point_y!=final_vertical_point[1]:
				while actual_point_x!=final_horizontal_point_x:
					# pygame.draw.rect(surface, "white", (actual_point_x, actual_point_y, 1, 1))
					# actual_point_x += vector_ortogonal_x+final_horizontal_point_x
					actual_point_x += 1
					# actual_point_y += vector_ortogonal_y+final_horizontal_point_y
					# actual_point_y = (actual_point_x-box_down_left_x)*vector_ortogonal_y/vector_ortogonal_x+box_down_left_y

				actual_point_x += vector_principal_x+box_up_left_x
				actual_point_y += vector_principal_y+box_up_left_y
				# 	final_horizontal_point_x += vector_principal_x+final_vertical_point[0]
				# 	final_horizontal_point_y += vector_principal_y+final_vertical_point[1]

				# pygame.draw.rect(surface, "white", (actual_point_x + vector_ortogonal_x, actual_point_y + vector_ortogonal_y, 1, 1))

def main():
	# points = [[Point(c, r) for c in range(WIDTH)] for r in range(HEIGHT)]
	circles = [
		Circle(i, CIRCLES[i]["x"], CIRCLES[i]["y"], CIRCLES[i]["r"], CIRCLES[i]["l"], CIRCLES[i]["c"]) for i in range(len(CIRCLES))
	]
	# classify_points(points, circles)
	paint = False

	running = True
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				if event.key == pygame.K_LSHIFT:
					paint = True

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LSHIFT:
					paint = False
			if event.type == pygame.MOUSEBUTTONUP:
				circle_move_index = -1

			if event.type == pygame.MOUSEBUTTONDOWN:
				if paint:
					handle_mouse_click(event.pos[0], event.pos[1], circles)
				else:
					for circle in circles:
						if distance_between_points(event.pos[0], event.pos[1], circle.x, circle.y) < circle.r:
							circle_move_index = circle.i

			if event.type == pygame.MOUSEMOTION:
				if event.buttons[0] != 1 or circle_move_index == -1: continue

				circles[circle_move_index].x = event.pos[0]
				circles[circle_move_index].y = event.pos[1]

		surface.fill(BACKGROUND_COLOR)

		circles_intersections(circles)
		draw_circles(surface, circles)

		pygame.display.flip()

		clock.tick(FRAMERATE)

	pygame.quit()

main()