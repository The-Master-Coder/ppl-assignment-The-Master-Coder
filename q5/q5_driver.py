from boys import Boy
from girls import Girl
from couple import Couple
from gifts import Gift
from utility import utility
from gift_essential import EssentialGift
from gift_luxury import LuxuryGift
from gift_utility import UtilityGift
from girl_choosy import ChoosyGirl
from girl_normal import NormalGirl
from girl_desperate import DesperateGirl
from boy_miser import MiserBoy
from boy_generous import GenerousBoy
from boy_geek import GeekBoy
from random import randint
import csv
import logging
from math import exp, log10

logging.basicConfig(format='%(asctime)s %(name)-6s %(levelname) s: %(message)s',
					datefmt='%d/%m/%Y %I:%M:%S %p',
					level=logging.DEBUG,
                    filename='log.txt',
                    filemode='w')

def allocate():
	'reads and stores the input from the boys.csv and girls.csv files and then makes the valid couples'

	B = []
	G = []
	CP = []

	with open('boys.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			if (row[5] == 'Miser'):
				B.append(MiserBoy(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), row[5]))
			elif (row[5] == 'Generous'):
				B.append(GenerousBoy(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), row[5]))
			else:
				B.append(GeekBoy(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), row[5]))
		csvfile.close()

	with open('girls.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			if (row[4] == 'Choosy'):
				G.append(ChoosyGirl(row[0], int(row[1]), int(row[2]), int(row[3]), row[4]))
			elif (row[4] == 'Normal'):
				G.append(NormalGirl(row[0], int(row[1]), int(row[2]), int(row[3]), row[4]))
			else:
				G.append(DesperateGirl(row[0], int(row[1]), int(row[2]), int(row[3]), row[4]))
		csvfile.close()

	B1 = sorted(B, key=lambda item: item.atr, reverse=True)
	B2 = sorted(B, key=lambda item: item.atr, reverse=True)
	G1 = sorted(G, key=lambda item: item.mbudget, reverse=True)
	SG = sorted(G, key=lambda item: item.atr, reverse=True)

	logging.warning('Check-out session going on ahead:\n')
	for i in range(5):
		if (i % 2 == 0):
			for g in G1:
				if (g.status == 'single'):
					break		
			for b in B1:
				logging.info('Commitment:  Girl: ' + g.name + '  is checking out  Boy: ' + b.name)
				if (b.is_elligible(g.mbudget, g.atr)) and (g.is_elligible(b.gfbudget)) and b.status == 'single':
					g.status = 'commited'
					b.status = 'commited'
					g.bfname = b.name
					b.gfname = g.name
					logging.info('Commitment:  Girl: ' + g.name + '  got commited with  Boy: ' + b.name)
					CP = CP+[(b, g)]
					break
			G1.remove(g)
		else:
			for b in B2:
				if (b.status == 'single'):
					break
			for g in SG:
				logging.info('Commitment:  Boy: ' + b.name + '  is checking out  Girl: ' + g.name)
				if (b.is_elligible(g.mbudget, g.atr)) and (g.is_elligible(b.gfbudget)) and g.status == 'single':
					g.status = 'commited'
					b.status = 'commited'
					g.bfname = b.name
					b.gfname = g.name
					logging.info('Commitment:  Boy: ' + b.name + '  got commited with  Girl: ' + g.name)
					CP = CP+[(b, g)]
					break
			B2.remove(b)

	print 'Couples formed (using new mechanism given in question 5):\n'
	for g in G:
		if g.status == 'single':
			print 'Girl: ' + g.name + '  is not commited to anyone'
		else:
			print 'Girl: ' + g.name + '  is commited with  Boy: ' + g.bfname

	print '\n'
	C = [Couple(c[0], c[1]) for c in CP]
	calculate_happiness(C)

def calculate_happiness(C):
	'reads and stores the inputs from the gifts.csv file and sorts the gifts in ascending order of price'
	GFT = []
	with open('gifts.csv', 'r') as csvfile:
		reader = csv.reader(csvfile, delimiter = ',')
		for row in reader:
			if (row[3] == 'Essential'):
				GFT.append(EssentialGift(row[0], int(row[1]), int(row[2]), row[3]))
			elif (row[5] == 'Luxury'):
				GFT.append(LuxuryGift(row[0], int(row[1]), int(row[2]), row[3], int(row[4]), int(row[5])))
			else:
				GFT.append(UtilityGift(row[0], int(row[1]), int(row[2]), row[3], int(row[4]), int(row[5])))
		csvfile.close()

	GFT = sorted(GFT, key=lambda item: item.price)
	logging.warning('Gifting session ahead:\n')
	for c in C:
		if (c.boy.type == 'Miser'):
			hp_miser(GFT, c)

		if (c.boy.type == 'Generous'):
			hp_generous(GFT, c)

		if (c.boy.type == 'Geek'):
			hp_geek(GFT, c)
	k = randint(1, len(C))
	print_hc(C, k)

def set_girl_happiness(c, v1, v2):
	if (c.girl.type == 'Choosy'):
		c.girl.happiness = log10(v2)
	elif (c.girl.type == 'Normal'):
		c.girl.happiness = v1
	else:
		c.girl.happiness = exp(v1)

def hp_miser(GFT, c):
	'provides gifting logic for Miser type Boys and sets the Happiness of the commited Boy and Girl and the whole couple, also sets the Compatibility of the couple'
	v1 = 0
	v2 = 0
	for g in GFT:
		if (g.price == c.girl.mbudget) or (g.price-c.girl.mbudget <= 100) and (c.boy.gfbudget >= 0) and (c.boy.gfbudget - g.price > 0):
			if (g.type == 'Luxury'):
				v2 = v2 + 2*g.price
			else:
				v2 = v2 + g.price
			v1 = v1 + g.price
			c.GFT = c.GFT + [g]
			c.boy.gfbudget = c.boy.gfbudget - g.price
			logging.info('Gifting:  Boy: ' + c.boy.name + '  gave his Girlfriend: ' + c.girl.name + '  Gift: ' + g.name + ' of price = ' + str(g.price) + ' rupees')

	set_girl_happiness(c, v1, v2)
	c.boy.happiness = c.boy.gfbudget
	c.set_happiness()
	c.set_compatibility()

def hp_generous(GFT, c):
	'provides gifting logic for Generous type Boys and sets the Happiness of the commited Boy and Girl and the whole couple, also sets the Compatibility of the couple'
	v1 = 0
	v2 = 0
	for g in GFT:
		if ((g.price == c.boy.gfbudget) or (c.boy.gfbudget-g.price <= 300)) and (c.boy.gfbudget >= 0) and (c.boy.gfbudget - g.price > 0):
			if (g.type == 'Luxury'):
				v2 = v2 + 2*g.price
			else:
				v2 = v2 + g.price
			v1 = v1 + g.price
			c.GFT = c.GFT + [g]
			c.boy.gfbudget = c.boy.gfbudget - g.price
			logging.info('Gifting:  Boy: ' + c.boy.name + '  gave his Girlfriend: ' + c.girl.name + '  Gift: ' + g.name + ' of price = ' + str(g.price) + ' rupees')
	
	set_girl_happiness(c, v1, v2)
	c.boy.happiness = c.girl.happiness
	c.set_happiness()
	c.set_compatibility()

def hp_geek(GFT, c):
	'provides gifting logic for Geek type Boys and sets the Happiness of the commited Boy and Girl and the whole couple, also sets the Compatibility of the couple'
	v1 = 0
	v2 = 0
	for g in GFT:
		if (g.price == c.girl.mbudget) or (g.price-c.girl.mbudget <= 100) and (c.boy.gfbudget >= 0) and (c.boy.gfbudget - g.price > 0):
			if (g.type == 'Luxury'):
				v2 = v2 + 2*g.price
			else:
				v2 = v2 + g.price
			v1 = v1 + g.price
			c.GFT = c.GFT + [g]
			c.boy.gfbudget = c.boy.gfbudget - g.price
			logging.info('Gifting:  Boy: ' + c.boy.name + '  gave his Girlfriend: ' + c.girl.name + '  Gift: ' + g.name + ' of price = ' + str(g.price) + ' rupees')

	for i in GFT:
		if (i not in c.GFT) and (i.type == 'luxury') and (i.price <= c.boy.gfbudget):
			v2 = v2 + 2*i.price
			v1 = v1 + i.price
			c.GFT = c.GFT + [i]
			c.boy.gfbudget = c.boy.gfbudget - i.price
			logging.info('Gifting:  Boy: ' + c.boy.name + '  gave his Girlfriend: ' + c.girl.name + '  Gift: ' + i.name + ' of price = ' + str(i.price) + ' rupees')
			break

	set_girl_happiness(c, v1, v2)
	c.boy.happiness = c.girl.intelli
	c.set_happiness()
	c.set_compatibility()

def print_hc(C, k):
	'prints the k most Happy Couples and k most Compatible Couples'
	A = sorted(C, key=lambda item: item.happiness, reverse=True)
	print str(k) + ' most Happy couples:'
	for i in range(k):
		print A[i].boy.name + ' and ' + A[i].girl.name

utility()
allocate()