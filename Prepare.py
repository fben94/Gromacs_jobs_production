	
import subprocess as sub
import time
import numpy as np
import math
import Utility
import os
import glob

#List of Lipids and Solvents:
LipidsList = ['DSPC','DPPC','DLPC']
SolventsList = ['W','OCO','PW']

#### WallParticlesList = ['','']

#***********************************************************#
#***********************************************************#
#********************* PDB Files list **********************#
#***********************************************************#
#***********************************************************#
PDBfileList = {'W':'water_single.pdb','OCO':'octanol_single.pdb',
			   'PW':'polwater_single.pdb','DSPC':'dspc_single.pdb',
			   'DPPC':'dppc_single.pdb','DLPC':'dlpc_single.pdb','SU':'su_single.pdb'}

W_PDB = """
		CRYST1   04.000   04.000   04.000  90.00  90.00  90.00 P1           1
		ATOM      1  W   W   X   1      00.000  00.000  00.000 0.00  0.00
		END
		"""

OCO_PDB = """
		CRYST1   10.000   10.000   10.000  90.00  90.00 90.00 P 1           1
		ATOM      1  PC  OCO     1      5.000  5.000  7.865 0.00  0.00          
		ATOM      2  C   OCO     1      5.000  5.000  3.135 0.00  0.00          
		END
		"""

PW_PDB = """
		CRYST1   52.237   82.455   48.563  90.00  90.00  90.00 P1           1
		ATOM      1  W   PW  X   1       8.010  77.839  11.290 0.00  0.00       
		ATOM      2  WP  PW  X   1       7.810  77.479  12.630 0.00  0.00       
		ATOM      3  WM  PW  X   1       9.260  78.329  11.680 0.00  0.00       
		END
		"""

DSPC_PDB = """
		CRYST1  125.000  125.000  100.000  90.00  90.00  90.00 P 1           1
		ATOM      1  NC3 DSPCX   2     105.980  90.400  72.500  0.00  0.00
		ATOM      2  PO4 DSPCX   2     105.630  90.710  69.500  0.00  0.00
		ATOM      3  GL1 DSPCX   2     105.780  90.260  66.500  0.00  0.00
		ATOM      4  GL2 DSPCX   2     107.160  90.030  66.500  0.00  0.00
		ATOM      5  C1A DSPCX   2     106.230  90.050  63.500  0.00  0.00
		ATOM      6  C2A DSPCX   2     105.920  90.250  60.500  0.00  0.00
		ATOM      7  C3A DSPCX   2     106.390  90.500  57.500  0.00  0.00
		ATOM      8  C4A DSPCX   2     106.320  90.710  54.500  0.00  0.00
		ATOM      9  C5A DSPCX   2     106.050  90.770  51.500  0.00  0.00
		ATOM     10  C1B DSPCX   2     108.660  89.710  63.500  0.00  0.00
		ATOM     11  C2B DSPCX   2     108.450  89.500  60.500  0.00  0.00
		ATOM     12  C3B DSPCX   2     108.130  88.940  57.500  0.00  0.00
		ATOM     13  C4B DSPCX   2     108.740  88.990  54.500  0.00  0.00
		ATOM     14  C5B DSPCX   2     108.540  89.120  51.500  0.00  0.00
		END
		"""

DPPC_PDB = """
		TITLE     DPPC sim
		REMARK    THIS IS A SIMULATION BOX
		CRYST1   30.000   30.000   30.000  90.00  90.00  90.00 P 1           1
		MODEL        1
		ATOM      1  NC3 DPPCX   1      13.368  14.653  25.970  1.00  0.00            
		ATOM      2  PO4 DPPCX   1      14.408  15.182  23.260  1.00  0.00            
		ATOM      3  GL1 DPPCX   1      13.608  14.862  19.630  1.00  0.00            
		ATOM      4  GL2 DPPCX   1      16.237  14.812  18.850  1.00  0.00            
		ATOM      5  C1A DPPCX   1      12.478  14.262  15.780  1.00  0.00            
		ATOM      6  C2A DPPCX   1      12.977  14.722  12.990  1.00  0.00            
		ATOM      7  C3A DPPCX   1      12.727  15.462  10.220  1.00  0.00            
		ATOM      8  C4A DPPCX   1      12.858  15.573   6.780  1.00  0.00            
		ATOM      9  C1B DPPCX   1      17.738  15.942  16.150  1.00  0.00            
		ATOM     10  C2B DPPCX   1      17.948  14.312  13.260  1.00  0.00            
		ATOM     11  C3B DPPCX   1      17.778  15.573  10.290  1.00  0.00            
		ATOM     12  C4B DPPCX   1      17.878  14.642   6.820  1.00  0.00            
		TER
		ENDMDL
		"""

DLPC_PDB = """
		CRYST1   30.000   30.000   30.000  90.00  90.00  90.00 P 1           1
		ATOM      1  NC3 DLPCX   1       5.560   4.860  23.400  1.00  0.00            
		ATOM      2  PO4 DLPCX   1       5.220   6.260  20.220  1.00  0.00            
		ATOM      3  GL1 DLPCX   1       4.840   5.200  16.780  1.00  0.00            
		ATOM      4  GL2 DLPCX   1       7.930   5.720  16.400  1.00  0.00            
		ATOM      5  C1A DLPCX   1       4.150   4.880  13.220  1.00  0.00            
		ATOM      6  C2A DLPCX   1       3.880   5.100  10.250  1.00  0.00            
		ATOM      7  C3A DLPCX   1       3.950   5.290   6.840  1.00  0.00            
		ATOM      8  C1B DLPCX   1       9.590   5.700  13.540  1.00  0.00            
		ATOM      9  C2B DLPCX   1       8.850   6.380  10.430  1.00  0.00            
		ATOM     10  C3B DLPCX   1       9.110   5.310   6.910  1.00  0.00            
		END
		"""
		
		
SU_PDB = """
		CRYST1   04.000   04.000   04.000  90.00  90.00  90.00 P1           1
		ATOM      1  TEMPSU  S   1      00.000  00.000  00.000 0.00  0.00
		END
		"""
		
#***********************************************************#
#***********************************************************#
#***********************************************************#

def InitBilayer(Sample, Softwares, GROMACS_LOC_prefixPath, PathToDefault):

	if 'DEFO' in Sample and not 'SU' in Sample: #Bilayer + Hole
		SHELL = 3.0
		
		LXS = Sample['LX']-SHELL
		LYS = Sample['LY']-SHELL
		LZS = Sample['LZ']-SHELL

		LZ2 = LZS/2.0
		
		#Number of lipid and water per layer
		NLM = {}
		NSOLM = {}
		
		LipidType = ''
		for L in LipidsList:
			if(L in Sample):
				NLM.update( {L:int(Sample[L]/2)} )
				LipidType = L
		for Sol in SolventsList:
			if(Sol in Sample):
				NSOLM.update( {Sol:int(Sample[Sol]/2)} )
				SolventType = Sol
		
		
		#=======================================================================
		# Setting the bilayers  ================================================
		#=======================================================================
		
		# DSPC bilayer =========================================================
		if LipidType == "DSPC":
			# Geometry to preprare the bilayer with packmol
			
			# total monolayer thickness (Angstrom)
			TMT = 30.0

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 7.0

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		# DPPC bilayer =========================================================
		if LipidType == "DPPC":
			# Geometry to preprare the bilayer with packmol
			# total monolayer thickness (Angstrom)
			TMT = 30
			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10
			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		# DLPC bilayer =========================================================
		if LipidType == "DLPC":
			# Geometry to preprare the bilayer with packmol

			# total monolayer thickness (Angstrom)
			TMT = 30

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		
		#=======================================================================
		#=======================================================================
		#=======================================================================
		
		#=======================================================================
		# Creating the defo ====================================================
		#=======================================================================
		
		if Sample['DEFO']['Height'] == 'box':
			L_defo = LZS
		if Sample['DEFO']['Height'] == 'bilayer':
			L_defo = M2headMAX - M1headMIN
		NbLayers = int(L_defo/float(Sample['DEFO']['DzDefo']))
		
		#Defo per Layer
		defoPerLayer = int(Sample['DEFO']['DpL']) + 1
		#Total number of defo
		nbDefo = defoPerLayer*NbLayers
		#Radius for the hole
		radiusDefo = float(Sample['DEFO']['Radius'])
		#Number of Solvent inside the hole
		#NbSolvIn = 0
		#if SolventType == 'W':
			## Density x Volume
			#NbSolvIn = int(8.26 * float(2*TMT*radiusDefo*radiusDefo*math.pi/1000.))
		#if SolventType == 'OCO':
			## Density x Volume
			#NbSolvIn = int(8.26 * float(2*TMT*radiusDefo*radiusDefo*math.pi/1000.)/2.)
		#if SolventType == 'PW':
			## Density x Volume
			#NbSolvIn = int(8.26 * float(2*TMT*radiusDefo*radiusDefo*math.pi/1000.)/3.)
		
		#Creating and Writing the defos configuration
		DefoXYZ_filename = 'defo.xyz'
		if os.path.exists(DefoXYZ_filename):
			os.remove(DefoXYZ_filename)
		XYZout = open(DefoXYZ_filename,"a")
		XYZout.write(str(nbDefo)+'\n\n')
		for i in range(0, NbLayers):
			ZcurrentDefo = float(Sample['DEFO']['DzDefo'])*i
			for i in np.arange(0., 360., 360./(defoPerLayer-1)):
				angle = math.radians(i)
				XYZout.write(Utility.RemoveUnwantedIndent(
					"""
					DEF  {0}  {1}  {2} \n
					""".format(radiusDefo*math.cos(angle), radiusDefo*math.sin(angle), ZcurrentDefo)
					))
			XYZout.write(Utility.RemoveUnwantedIndent(
					"""
					DEF  0.0 0.0 {0} \n
					""".format(ZcurrentDefo)
					))
		XYZout.close()
		
		#Formating the defos
		formatDEFO = open("format_DEFO.vmd","w")
		formatDEFO.write(Utility.RemoveUnwantedIndent(
			"""
			mol load xyz {0}
			set all [atomselect top "all"]
				
			$all set resname DEFO
			$all set name DEF
			$all set type DEF
			$all set chain X
				
			package require pbctools
			pbc set {{0.5 0.5 {1}}}
				
			$all writepdb {2}
			unset all
				
			exit
			""".format(DefoXYZ_filename, L_defo, DefoXYZ_filename.replace('xyz','pdb'))
			))
		formatDEFO.close()
		
		cmd = str("""{0} -dispdev text -e format_DEFO.vmd > format_DEFO.log""").format(Softwares['VMD'])
		sub.call(cmd, shell=True)
		
		#=======================================================================
		#=======================================================================
		#=======================================================================
		
		#=======================================================================
		# Setting the bilayers for packmol =====================================
		#=======================================================================
		
		#Setting the name of the system
		System = """{0}_{1}{2}_{3}{4}_{5}DEFO{6}""".format(Sample['TYPE'], 
													Sample[LipidType], 
													LipidType, 
													Sample[SolventType], 
													SolventType, nbDefo, 
													  Sample['DEFO']['Version'])
		
		# DLPC bilayer =========================================================
		if LipidType == "DSPC":
			PackmolInput = """
						#
						# Lipid bilayer with water, perpendicular to z axis
						#
						
						# Every atom from diferent molecules will be far from each other at
						# least 3.0 Anstroms at the solution.
						
						tolerance 3.0
						
						# Coordinate file types will be in pdb format (keyword not required for
						# pdb file format, but required for tinker, xyz or moldy)
						
						filetype pdb
						
						# do not avoid the fixed molecules
						#avoid_overlap no
						
						# The output pdb file
						
						output {0}.pdb
						
						structure {19}
							resnumbers 3
							number {1:g}
							inside box 0. 0. {2}  {3} {4} {5}
							atoms 1
								below plane 0. 0. 1. {6}
							end atoms
							atoms 9 14
								over plane 0. 0. 1. {7}
							end atoms
							outside cylinder  {15} {16}  {2}  0.  0.  1.  {18}  {17}
						end structure
						
						structure {19}
							resnumbers 3
							number {1:g}
							inside box 0. 0.  {8}  {3} {4} {9}
							atoms 1
								over plane 0. 0. 1. {10}
							end atoms
							atoms 9 14
								below plane 0. 0. 1. {11}
							end atoms
							outside cylinder  {15} {16}  {2}  0.  0.  1.  {18}  {17}
						end structure
						
						""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, 
									M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, 
									M2headMAX, M2headMIN, M2tailMAX, 
									NSOLM[SolventType], LZS, 
									DefoXYZ_filename.replace('xyz','pdb'), 
									LXS/2.0, LYS/2.0, L_defo, radiusDefo, 
									PDBfileList[LipidType], 
									PDBfileList[SolventType])
		
		# DPPC bilayer =========================================================
		if LipidType == 'DPPC':
			PackmolInput = """
						#
						# Lipid bilayer with water, perpendicular to z axis
						#
						
						# Every atom from diferent molecules will be far from each other at
						# least 3.0 Anstroms at the solution.
						
						tolerance 3.0
						
						# Coordinate file types will be in pdb format (keyword not required for
						# pdb file format, but required for tinker, xyz or moldy)
						
						filetype pdb
						
						# do not avoid the fixed molecules
						#avoid_overlap no
						
						# The output pdb file
						
						output {0}.pdb
						
						structure {18}
							resnumbers 3
							number {1:g}
							inside box 0. 0. {2}  {3} {4} {5}
							constrain_rotation x 180 10
							constrain_rotation y 180 10
							outside cylinder  {15} {16}  0.  0.  0.  1.  5.  {17}
						end structure
						
						structure {18}
							resnumbers 3
							number {1:g}
							inside box 0. 0.  {8}  {3} {4} {9}
							constrain_rotation x 0 10
							constrain_rotation y 0 10
							outside cylinder  {15} {16}  0.  0.  0.  1.  5.  {17}
						end structure
						
						""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, DefoXYZ_filename.replace('xyz','pdb'), LXS/2.0, LYS/2.0, Sample['LZ'], PDBfileList[LipidType], PDBfileList[SolventType])
		
		# DLPC bilayer =========================================================
		if LipidType == 'DLPC':
			PackmolInput = """
						#
						# Lipid bilayer with water, perpendicular to z axis
						#
						
						# Every atom from diferent molecules will be far from each other at
						# least 3.0 Anstroms at the solution.
						
						tolerance 3.0
						
						# Coordinate file types will be in pdb format (keyword not required for
						# pdb file format, but required for tinker, xyz or moldy)
						
						filetype pdb
						
						# do not avoid the fixed molecules
						#avoid_overlap no
						
						# The output pdb file
						
						output {0}.pdb
						
						structure {18}
							resnumbers 3
							number {1:g}
							inside box 0. 0. {2}  {3} {4} {5}
							constrain_rotation x 180 10
							constrain_rotation y 180 10
							outside cylinder  {15} {16}  0.  0.  0.  1.  5.  {17}
						end structure
						
						structure {18}
							resnumbers 3
							number {1:g}
							inside box 0. 0.  {8}  {3} {4} {9}
							constrain_rotation x 0 10
							constrain_rotation y 0 10
							outside cylinder  {15} {16}  0.  0.  0.  1.  5.  {17}
						end structure
						
						""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, DefoXYZ_filename.replace('xyz','pdb'), LXS/2.0, LYS/2.0, Sample['LZ'], PDBfileList[LipidType], PDBfileList[SolventType])
		
		#=======================================================================
		#=======================================================================
		#=======================================================================
		
		#=======================================================================
		# Setting the defo with solvent for packmol ============================
		#=======================================================================
		
		if SolventType == 'PW':
			PackmolInput += """
			
							structure {15}
								number {12:g}
								inside box 0. 0. 0.  {3} {4} {2}
								atoms 2 3
									radius 0.2
								end atoms
							end structure


							structure {15}
								number {12:g}
								inside box 0. 0. {9}  {3} {4} {13}
								atoms 2 3
									radius 0.2
								end atoms
							end structure
							
							structure {14}
								chain X
								number 1
								resnumbers 3
								fixed {15} {16} 0.0 0.0 0.0 0.0
							end structure
					
					""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, 
								M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, 
								M2headMAX, M2headMIN, M2tailMAX, 
								NSOLM[SolventType], LZS, 
								DefoXYZ_filename.replace('xyz','pdb'), 
								LXS/2.0, LYS/2.0, L_defo, 
								PDBfileList[LipidType], 
								PDBfileList[SolventType])
		else:
			PackmolInput += """
							
							structure {20}
								chain C
								number {12:g}
								inside box 0. 0. 0.  {3} {4} {2}
							end structure
							
							structure {20}
								chain D
								number {12:g}
								inside box 0. 0. {9}  {3} {4} {13}
							end structure
							
							structure {14}
								chain X
								number 1
								resnumbers 3
								fixed {15} {16} {21} 0.0 0.0 0.0
								radius 0.
							end structure
							
					""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, 
								M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, 
								M2headMAX, M2headMIN, M2tailMAX, 
								NSOLM[SolventType], LZS, 
								DefoXYZ_filename.replace('xyz','pdb'), 
								LXS/2.0, LYS/2.0, L_defo, radiusDefo, 
								PDBfileList[LipidType], 
								PDBfileList[SolventType], 
								M1headMIN)
						
			f = open('packmol_'+System+'.input','w')
			f.write(Utility.RemoveUnwantedIndent(PackmolInput))
			f.close()
		
		# Lipids input pdb =====================================================
		if( LipidType == "DSPC"):
			f = open('dspc_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(DSPC_PDB))
			f.close()
		if( LipidType == "DPPC"):
			f = open('dppc_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(DPPC_PDB))
			f.close()
		if( LipidType == "DLPC"):
			f = open('dlpc_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(DLPC_PDB))
			f.close()
			
		# Solvents input pdb ===================================================
		if( SolventType == 'W'):
			f = open('water_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(W_PDB))
			f.close()
		if( SolventType == 'PW'):
			f = open('polwater_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(PW_PDB))
			f.close()
		if( SolventType == 'OCO'):
			f = open('octanol_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(OCO_PDB))
			f.close()
		
		#=======================================================================
		#lauching packmol
		#=======================================================================

		cmd = str("""{0} < packmol_{1}.input > packmol_{1}.output """
								).format(Softwares['PACKMOL'],System)
		sub.call(cmd, shell=True)

		#=======================================================================
		# ensure the right box in pdb file
		#=======================================================================

		WriteBox = str("""
				mol load pdb {0}.pdb
				set all [atomselect top "all"]

				package require pbctools
				pbc set {{{1} {2} {3}}}

				$all writepdb "{0}.withbox.pdb"
				unset all

				exit
				""").format(System, Sample['LX'], Sample['LY'], Sample['LZ'])

		f = open('write_box.vmd','w+')
		f.write(Utility.RemoveUnwantedIndent(WriteBox) )
		f.close()

		## ======================================================================
		cmd = str("""{0} -dispdev text -e write_box.vmd > write_box.log"""
												).format(Softwares['VMD'])
		sub.call(cmd, shell=True)
		
		MakeIndex = str("""
				chain A
				name 5 up{0}
				chain B
				name 6 low{0}
				chain C
				name 7 low{1}
				chain D
				name 8 up{1}
				chain X
				name 9 defo
				q
				
				""").format(LipidType,SolventType)

		f = open('make_index.input','w+')
		f.write(Utility.RemoveUnwantedIndent(MakeIndex) )
		f.close()
		
		cmd = str("""{0}make_ndx -f {1}.withbox.pdb -o {1}.ndx < make_index.input"""
											).format(GROMACS_LOC_prefixPath, System)
		sub.call(cmd, shell=True)
		
		#=======================================================================
		# the topology file
		#=======================================================================
		TopologyDefo(Sample, PathToDefault)
		
		Topology = str("""
					#include "martini_v2.2_DEFO_{0}.itp"
					#include "martini_v2.0_lipids.itp"
					""".format(Sample['DEFO']['Version']))
		
		#Copy the topology files for martini forcefield
		sub.call("""cp {0}/martini_v2.0_lipids.itp  .""".format(PathToDefault), shell= True)
		sub.call("""cp {0}/DEFO/defo_posres.itp  .""".format(PathToDefault), shell= True)
		f = open(System+'.top','w')
		f.write(Utility.RemoveUnwantedIndent(Topology))

		f = open(System+'.top','a')
		f.write("""\n[ system ]\n""")

		Topology = str("""{0}_{1}_WITH_DEFO_{2}\n""").format(LipidType, Sample['TYPE'], Sample['DEFO']['Version'])
		f.write(Topology)

		f.write("""\n[ molecules ]\n""")
		Topology = str("""{0} {1}\n{2} {3}\n{4} {5}\n""").format(LipidType, Sample[LipidType], SolventType, Sample[SolventType],'DEFO',nbDefo)
		f.write(Topology)
		f.close()
		
		Output = str("""{0}.withbox.pdb""").format(System)
		Index = str("""{0}.ndx""").format(System)
		return { 'SYSTEM': System, 'OUTPUT': Output, 'INDEX':Index}

	################################################################################
	################################################################################
	################################################################################
	################################################################################


	if 'SU' in Sample and not 'DEFO' in Sample: #Bilayer + Wall:
		THICKNESS = float(Sample['SU']['Thickness'])
		DENSITY = float(Sample['SU']['Density'])
		NBLIPIDS_MONO = int(Sample['SU']['NbLipidsM'])
		SU_VERSION = Sample['SU']['Version']
		SU_TYPE = Sample['SU']['SuType']
		LZM = float(Sample['SU']['LzM'])
		
		
		SHELL = 3.0
		LXS = Sample['LX'] - SHELL
		LYS = Sample['LY'] - SHELL
		LZS = LZM + THICKNESS

		LZ2 = LZS/2.0
		

		#Number of lipid and water per layer
		NLM = {}
		NSOLM = {}
		LipidType = ''
		
		for L in LipidsList:
			if(L in Sample):
				NLM.update( {L:int(Sample[L]/2)} )
				LipidType = L
				
		for Sol in SolventsList:
			print(Sol,' is in sample:', Sol in Sample)
			if Sol in Sample:
				print(Sol)
				NSOLM.update( {Sol:int(Sample[Sol]/2)} )
				SolventType = Sol
				
		#Computing the number of SU
		nbSu = int( DENSITY * Sample['LX'] * Sample['LY'] * THICKNESS /1000 )
		
		#=======================================================================
		# Setting the bilayers  ================================================
		#=======================================================================
		
		# DSPC bilayer =========================================================
		if LipidType == "DSPC":
			# Geometry to preprare the bilayer with packmol
			
			# total monolayer thickness (Angstrom)
			TMT = 30.0

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 7.0

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		# DPPC bilayer =========================================================
		if LipidType == "DPPC":
			# Geometry to preprare the bilayer with packmol
			# total monolayer thickness (Angstrom)
			TMT = 30.0
			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10
			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		# DLPC bilayer =========================================================
		if LipidType == "DLPC":
			# Geometry to preprare the bilayer with packmol

			# total monolayer thickness (Angstrom)
			TMT = 30.0

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		
		#=======================================================================
		#=======================================================================
		#=======================================================================

		System = str('{0}_{1}{2}_{3}M{2}_{4}{5}_{7}{6}{8}').format(Sample['TYPE'], Sample[LipidType],
												LipidType, NBLIPIDS_MONO , 
												Sample[SolventType], SolventType, SU_TYPE, nbSu, SU_VERSION)
		
		#=======================================================================
		# Setting the bilayers for packmol =====================================
		#=======================================================================
		
		# DLPC bilayer =========================================================
		if LipidType == "DSPC":
			PackmolInput = """
						#
						# Lipid bilayer with water, perpendicular to z axis
						#
						
						# Every atom from diferent molecules will be far from each other at
						# least 3.0 Anstroms at the solution.
						
						tolerance 3.0
						
						# Coordinate file types will be in pdb format (keyword not required for
						# pdb file format, but required for tinker, xyz or moldy)
						
						filetype pdb
						
						# do not avoid the fixed molecules
						#avoid_overlap no
						
						# The output pdb file
						
						output {0}.pdb
						
						structure {14}
							chain A
							resnumbers 3
							number {1:g}
							inside box 0. 0. {2}  {3} {4} {5}
							atoms 1
								below plane 0. 0. 1. {6}
							end atoms
							atoms 9 14
								over plane 0. 0. 1. {7}
							end atoms
						end structure
						
						structure {14}
							chain B
							resnumbers 3
							number {1:g}
							inside box 0. 0.  {8}  {3} {4} {9}
							atoms 1
								over plane 0. 0. 1. {10}
							end atoms
							atoms 9 14
								below plane 0. 0. 1. {11}
							end atoms
						end structure
						
						""".format(System, NLM[LipidType], M1headMIN, LXS,
									LYS, M1tailMAX, M1headMAX, M1tailMIN, 
									M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
									NSOLM[SolventType], LZS, PDBfileList[LipidType])
						
			PackmolInput += """
						
						structure {5}
							chain C
							resnumbers 3
							number {6:g}
							inside box 0. 0.  {7}  {0} {1} {2}
							atoms 1
								below plane 0. 0. 1. {3}
							end atoms
							atoms 9 14
								over plane 0. 0. 1. {4}
							end atoms
						end structure
						
						""".format(LXS, LYS, M1tailMAX+LZM, LZM+DZ, TMT+LZM-DZ, PDBfileList[LipidType], NBLIPIDS_MONO , LZM)
		
		# DPPC bilayer =========================================================
		if LipidType == 'DPPC':
			PackmolInput = """
							#
							# Lipid bilayer with water, perpendicular to z axis
							#

							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.

							tolerance 3.0

							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)

							filetype pdb

							# The output pdb file

							output {0}.pdb

							structure {14}
								chain A
								resnumbers 3
								number {1:g}
								inside box 0. 0. {2}  {3} {4} {5}
								constrain_rotation x 180 10
								constrain_rotation y 180 10
							end structure

							structure {14}
								chain B
								resnumbers 3
								number {1:g}
								inside box 0. 0.  {8}  {3} {4} {9}
								constrain_rotation x 0 10
								constrain_rotation y 0 10
							end structure

							""".format(System, NLM[LipidType], M1headMIN, LXS, 
				  						LYS, M1tailMAX, M1headMAX, M1tailMIN, 
				  						M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
				  						NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
			
			PackmolInput += """
						
						structure {3}
							chain C
							resnumbers 3
							number {4:g}
							inside box 0. 0.  {5}  {0} {1} {2}
							constrain_rotation x 180 10
							constrain_rotation y 180 10
						end structure
						
						""".format(LXS, LYS, TMT+LZM, PDBfileList[LipidType], NBLIPIDS_MONO , LZM)
		
		# DLPC bilayer =========================================================
		if LipidType == 'DLPC':
			PackmolInput = """
							#
							# Lipid bilayer with water, perpendicular to z axis
							#

							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.

							tolerance 3.0

							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)

							filetype pdb

							# The output pdb file

							output {0}.pdb

							structure {14}
							chain A
								resnumbers 3
								number {1:g}
								inside box 0. 0. {2}  {3} {4} {5}
								constrain_rotation x 180 10
								constrain_rotation y 180 10
							end structure

							structure {14}
								chain B
								resnumbers 3
								number {1:g}
								inside box 0. 0.  {8}  {3} {4} {9}
								constrain_rotation x 0 10
								constrain_rotation y 0 10
							end structure
							""".format(System, NLM[LipidType], M1headMIN, LXS, 
										LYS, M1tailMAX, M1headMAX, M1tailMIN, 
										M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
										NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
							
			PackmolInput += """
						
						structure {3}
							chain C
							resnumbers 3
							number {4:g}
							inside box 0. 0.  {5}  {0} {1} {2}
							constrain_rotation x 180 10
							constrain_rotation y 180 10
						end structure
						
						""".format(LXS, LYS, TMT+LZM, PDBfileList[LipidType], NBLIPIDS_MONO , LZM)
		
		#=======================================================================
		#=======================================================================
		#=======================================================================

		#=======================================================================
		# Setting the defo with solvent for packmol ============================
		#=======================================================================
		
		if SolventType == 'PW':
			PackmolInput += """
			
							structure {15}
								chain D
								number {12:g}
								inside box 0. 0. 0.  {3} {4} {2}
								atoms 2 3
									radius 0.2
								end atoms
							end structure


							structure {15}
								chain E
								number {12:g}
								inside box 0. 0. {9}  {3} {4} {13}
								atoms 2 3
									radius 0.2
								end atoms
							end structure
					
					""".format(System, NLM[LipidType], M1headMIN, LXS, 
								LYS, M1tailMAX, M1headMAX, M1tailMIN,
								M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
								NSOLM[SolventType], LZS, PDBfileList[SolventType])
		else:
			PackmolInput += """
						
						structure {14}
							chain D
							number {12:g}
							inside box 0. 0. {16}  {3} {4} {2}
						end structure
						
						structure {14}
							chain E
							number {12:g}
							inside box 0. 0. {9}  {3} {4} {13}
						end structure
						
						
						""".format(System, NLM[LipidType], M1headMIN, LXS, 
								LYS, M1tailMAX, M1headMAX, M1tailMIN,
								M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
								NSOLM[SolventType], LZM, PDBfileList[SolventType], M1headMIN, THICKNESS)
						
		
			
		# Adding the substrat
		
		PackmolInput += """
						
						structure {4}
							chain S
							number {3:g}
							inside box 0. 0. 0.  {0} {1} {2}
						end structure
						
						
						""".format(LXS, LYS, THICKNESS, nbSu, PDBfileList['SU'])
		
		f = open('packmol_'+System+'.input','w')
		f.write(Utility.RemoveUnwantedIndent(PackmolInput))
		f.close()
		
		# Lipids input pdb =====================================================
		if( LipidType == "DSPC"):
			f = open(PDBfileList['DSPC'],'w')
			f.write(Utility.RemoveUnwantedIndent(DSPC_PDB))
			f.close()
		if( LipidType == "DPPC"):
			f = open(PDBfileList['DPPC'],'w')
			f.write(Utility.RemoveUnwantedIndent(DPPC_PDB))
			f.close()
		if( LipidType == "DLPC"):
			f = open(PDBfileList['DLPC'],'w')
			f.write(Utility.RemoveUnwantedIndent(DLPC_PDB))
			f.close()
			
		# Solvents input pdb ===================================================
		if( SolventType == 'W'):
			f = open(PDBfileList['W'],'w')
			f.write(Utility.RemoveUnwantedIndent(W_PDB))
			f.close()
		if( SolventType == 'PW'):
			f = open(PDBfileList['PW'],'w')
			f.write(Utility.RemoveUnwantedIndent(PW_PDB))
			f.close()
		if( SolventType == 'OCO'):
			f = open(PDBfileList['OCO'],'w')
			f.write(Utility.RemoveUnwantedIndent(OCO_PDB))
			f.close()
			
		# pdb file for su
		suType = SU_TYPE
		if len(SU_TYPE) < 4:
			suType = SU_TYPE + (4 - len(SU_TYPE))*' '
		suPdb = SU_PDB.replace("TEMP", suType)
		f = open(PDBfileList['SU'],'w')
		f.write(Utility.RemoveUnwantedIndent(suPdb))
		f.close()
			
			
		#=======================================================================
		#lauching packmol
		#=======================================================================

		cmd = str("""{0} < packmol_{1}.input > packmol_{1}.output """
								).format(Softwares['PACKMOL'], System)
		sub.call(cmd, shell=True)

		#=======================================================================
		# ensure the right box in pdb file
		#=======================================================================

		WriteBox = str("""
				mol load pdb {0}.pdb
				set all [atomselect top "all"]

				package require pbctools
				pbc set {{{1} {2} {3}}}

				$all writepdb "{0}.withbox.pdb"
				unset all

				exit
				""").format(System, Sample['LX'], Sample['LY'], Sample['LZ'])

		f = open('write_box.vmd','w+')
		f.write(Utility.RemoveUnwantedIndent(WriteBox) )
		f.close()

		## ======================================================================
		cmd = str("""{0} -dispdev text -e write_box.vmd > write_box.log"""
												).format(Softwares['VMD'])
		sub.call(cmd, shell=True)
		
		MakeIndex = str("""
				chain A
				name 5 up{0}
				chain B
				name 6 low{0}
				chain C
				name 7 mono{0}
				chain D
				name 8 up{1}
				chain E
				name 9 low{1}
				chain S
				name 10 su
				q
				
				""").format(LipidType, SolventType)

		f = open('make_index.input','w+')
		f.write(Utility.RemoveUnwantedIndent(MakeIndex) )
		f.close()
		
		cmd = str("""{0}make_ndx -f {1}.withbox.pdb -o {1}.ndx < make_index.input"""
											).format(GROMACS_LOC_prefixPath, System)
		sub.call(cmd, shell=True)
		
		
		#=======================================================================
		# the topology file
		#=======================================================================
		TopologySu(Sample, PathToDefault)
		
		Topology = """
					#include "martini_v2.2_{1}_{0}.itp"
					#include "martini_v2.0_lipids.itp"
					
					""".format(Sample['SU']['Version'], SU_TYPE)
		
		#Copy the topology files for martini forcefield
		sub.call("""cp {0}/martini_v2.0_lipids.itp  .""".format(PathToDefault), shell= True)
		sub.call("""cp {0}/SU/su_posres.itp  .""".format(PathToDefault), shell= True)
		f = open(System+'.top','w')
		f.write(Utility.RemoveUnwantedIndent(Topology))

		f = open(System+'.top','a')
		f.write("""\n[ system ]\n""")

		Topology = str("""{0}_{1}_WITH_{3}_{2}\n""").format(LipidType, Sample['TYPE'], Sample['SU']['Version'], SU_TYPE)
		f.write(Topology)

		f.write("""\n[ molecules ]\n""")
		Topology = str("""{0} {1}\n{2} {3}\n{4} {5}\n""").format(LipidType, Sample[LipidType]+NBLIPIDS_MONO, SolventType, Sample[SolventType], SU_TYPE, nbSu)
		f.write(Topology)
		f.close()
			
		#==================================================================================
		# Output the files for other steps
		#==================================================================================
		Output = str("""{0}.withbox.pdb""").format(System)
		Index = str("""{0}.ndx""").format(System)
		return { 'SYSTEM': System, 'OUTPUT': Output, 'INDEX':Index}


	################################################################################
	################################################################################
	################################################################################
	################################################################################


	if 'DEFO' in Sample and 'SU' in Sample: #Bilayer + Hole + Wall:
		THICKNESS = float(Sample['SU']['Thickness'])
		DENSITY = float(Sample['SU']['Density'])
		NBLIPIDS_MONO = int(Sample['SU']['NbLipidsM'])
		SU_VERSION = Sample['SU']['Version']
		SU_TYPE = Sample['SU']['SuType']
		LZM = float(Sample['SU']['LzM'])
		
		
		SHELL = 3.0
		LXS = Sample['LX'] - SHELL
		LYS = Sample['LY'] - SHELL
		LZS = LZM + THICKNESS

		LZ2 = LZS/2.0
		

		#Number of lipid and water per layer
		NLM = {}
		NSOLM = {}
		LipidType = ''
		
		for L in LipidsList:
			if(L in Sample):
				NLM.update( {L:int(Sample[L]/2)} )
				LipidType = L
				
		for Sol in SolventsList:
			print(Sol,' is in sample:', Sol in Sample)
			if Sol in Sample:
				print(Sol)
				NSOLM.update( {Sol:int(Sample[Sol]/2)} )
				SolventType = Sol
		
		#=======================================================================
		# Setting the bilayers  ================================================
		#=======================================================================
		
		# DSPC bilayer =========================================================
		if LipidType == "DSPC":
			# Geometry to preprare the bilayer with packmol
			
			# total monolayer thickness (Angstrom)
			TMT = 30.0

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 7.0

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		# DPPC bilayer =========================================================
		if LipidType == "DPPC":
			# Geometry to preprare the bilayer with packmol
			# total monolayer thickness (Angstrom)
			TMT = 30.0
			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10
			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		# DLPC bilayer =========================================================
		if LipidType == "DLPC":
			# Geometry to preprare the bilayer with packmol

			# total monolayer thickness (Angstrom)
			TMT = 30.0

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
		
		
		#=======================================================================
		# Creating the defo ====================================================
		#=======================================================================
		
		if Sample['DEFO']['Height'] == 'box':
			L_defo = LZS + TMT
		if Sample['DEFO']['Height'] == 'bilayer':
			L_defo = M2headMAX - M1headMIN
		NbLayers = int(L_defo/float(Sample['DEFO']['DzDefo']))
		
		#Defo per Layer
		defoPerLayer = int(Sample['DEFO']['DpL']) + 1
		#Total number of defo
		nbDefo = defoPerLayer*NbLayers
		#Radius for the hole
		radiusDefo = float(Sample['DEFO']['Radius'])
		#Number of Solvent inside the hole
		#NbSolvIn = 0
		#if SolventType == 'W':
			## Density x Volume
			#NbSolvIn = int(8.26 * float(2*TMT*radiusDefo*radiusDefo*math.pi/1000.))
		#if SolventType == 'OCO':
			## Density x Volume
			#NbSolvIn = int(8.26 * float(2*TMT*radiusDefo*radiusDefo*math.pi/1000.)/2.)
		#if SolventType == 'PW':
			## Density x Volume
			#NbSolvIn = int(8.26 * float(2*TMT*radiusDefo*radiusDefo*math.pi/1000.)/3.)
		
		#Creating and Writing the defos configuration
		DefoXYZ_filename = 'defo.xyz'
		if os.path.exists(DefoXYZ_filename):
			os.remove(DefoXYZ_filename)
		XYZout = open(DefoXYZ_filename,"a")
		XYZout.write(str(nbDefo)+'\n\n')
		for i in range(0, NbLayers):
			ZcurrentDefo = float(Sample['DEFO']['DzDefo'])*i
			for i in np.arange(0., 360., 360./(defoPerLayer-1)):
				angle = math.radians(i)
				XYZout.write(Utility.RemoveUnwantedIndent(
					"""
					DEF  {0}  {1}  {2} \n
					""".format(radiusDefo*math.cos(angle), radiusDefo*math.sin(angle), ZcurrentDefo)
					))
			XYZout.write(Utility.RemoveUnwantedIndent(
					"""
					DEF  0.0 0.0 {0} \n
					""".format(ZcurrentDefo)
					))
		XYZout.close()
		
		#Formating the defos
		formatDEFO = open("format_DEFO.vmd","w")
		formatDEFO.write(Utility.RemoveUnwantedIndent(
			"""
			mol load xyz {0}
			set all [atomselect top "all"]
				
			$all set resname DEFO
			$all set name DEF
			$all set type DEF
			$all set chain X
				
			package require pbctools
			pbc set {{0.5 0.5 {1}}}
				
			$all writepdb {2}
			unset all
				
			exit
			""".format(DefoXYZ_filename, L_defo, DefoXYZ_filename.replace('xyz','pdb'))
			))
		formatDEFO.close()
		
		cmd = str("""{0} -dispdev text -e format_DEFO.vmd > format_DEFO.log""").format(Softwares['VMD'])
		sub.call(cmd, shell=True)
		
		#=======================================================================
		# Number of su particles ===============================================
		#=======================================================================
		nbSu = int( DENSITY * Sample['LX'] * Sample['LY'] * THICKNESS /1000 )
		
		#=======================================================================
		#=======================================================================
		#=======================================================================
		
		#=======================================================================
		#=======================================================================
		#=======================================================================

		System = str('{0}_{1}{2}_{3}M{2}_{4}{5}_{6}DEFO{7}_{8}{10}{9}').format(Sample['TYPE'], Sample[LipidType],
												LipidType, NBLIPIDS_MONO , 
												Sample[SolventType], SolventType,
												nbDefo, Sample['DEFO']['Version'], nbSu, Sample['SU']['Version'],SU_TYPE)
		
		#=======================================================================
		# Setting the bilayers for packmol =====================================
		#=======================================================================
		
		# DLPC bilayer =========================================================
		if LipidType == "DSPC":
			PackmolInput = """
						#
						# Lipid bilayer with water, perpendicular to z axis
						#
						
						# Every atom from diferent molecules will be far from each other at
						# least 3.0 Anstroms at the solution.
						
						tolerance 3.0
						
						# Coordinate file types will be in pdb format (keyword not required for
						# pdb file format, but required for tinker, xyz or moldy)
						
						filetype pdb
						
						# do not avoid the fixed molecules
						#avoid_overlap no
						
						# The output pdb file
						
						output {0}.pdb
						
						structure {14}
							chain A
							resnumbers 3
							number {1:g}
							inside box 0. 0. {2}  {3} {4} {5}
							atoms 1
								below plane 0. 0. 1. {6}
							end atoms
							atoms 9 14
								over plane 0. 0. 1. {7}
							end atoms
							outside cylinder  {15} {16}  {2}  0.  0.  1.  {18}  {17}
						end structure
						
						structure {14}
							chain B
							resnumbers 3
							number {1:g}
							inside box 0. 0.  {8}  {3} {4} {9}
							atoms 1
								over plane 0. 0. 1. {10}
							end atoms
							atoms 9 14
								below plane 0. 0. 1. {11}
							end atoms
							outside cylinder  {15} {16}  {19}  0.  0.  1.  {18}  {17}
						end structure
						
						""".format(System, NLM[LipidType], M1headMIN, LXS,
									LYS, M1tailMAX, M1headMAX, M1tailMIN, 
									M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
									NSOLM[SolventType], LZS, PDBfileList[LipidType], 
									LXS/2.0, LYS/2.0, L_defo, radiusDefo, THICKNESS)
						
			PackmolInput += """
						
						structure {5}
							chain C
							resnumbers 3
							number {6:g}
							inside box 0. 0.  {7}  {0} {1} {2}
							atoms 1
								below plane 0. 0. 1. {3}
							end atoms
							atoms 9 14
								over plane 0. 0. 1. {4}
							end atoms
							outside cylinder  {8} {9}  {12}  0.  0.  1.  {11}  {10}
						end structure
						
						""".format(LXS, LYS, M1tailMAX+LZM, LZM+DZ, TMT+LZM-DZ, 
								PDBfileList[LipidType], NBLIPIDS_MONO , LZM, LXS/2.0,
								LYS/2.0, L_defo, radiusDefo, THICKNESS)
		
		# DPPC bilayer =========================================================
		if LipidType == 'DPPC':
			PackmolInput = """
							#
							# Lipid bilayer with water, perpendicular to z axis
							#

							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.

							tolerance 3.0

							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)

							filetype pdb

							# The output pdb file

							output {0}.pdb

							structure {14}
								chain A
								resnumbers 3
								number {1:g}
								inside box 0. 0. {2}  {3} {4} {5}
								constrain_rotation x 180 10
								constrain_rotation y 180 10
								outside cylinder  {15} {16}  {19}  0.  0.  1.  {18}  {17}
							end structure

							structure {14}
								chain B
								resnumbers 3
								number {1:g}
								inside box 0. 0.  {8}  {3} {4} {9}
								constrain_rotation x 0 10
								constrain_rotation y 0 10
								outside cylinder  {15} {16}  {19}  0.  0.  1.  {18}  {17}
							end structure

							""".format(System, NLM[LipidType], M1headMIN, LXS, 
										LYS, M1tailMAX, M1headMAX, M1tailMIN, 
										M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
										NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType], 
										LXS/2.0, LYS/2.0, L_defo, radiusDefo, THICKNESS)
			
			PackmolInput += """
						
						structure {3}
							chain C
							resnumbers 3
							number {4:g}
							inside box 0. 0.  {5}  {0} {1} {2}
							constrain_rotation x 180 10
							constrain_rotation y 180 10
							outside cylinder  {8} {9}  {12}  0.  0.  1.  {11}  {10}
						end structure
						
						""".format(LXS, LYS, TMT+LZM, PDBfileList[LipidType], NBLIPIDS_MONO , LZM, 
									LXS/2.0, LYS/2.0, L_defo, radiusDefo, THICKNESS)
		
		# DLPC bilayer =========================================================
		if LipidType == 'DLPC':
			PackmolInput = """
							#
							# Lipid bilayer with water, perpendicular to z axis
							#

							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.

							tolerance 3.0

							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)

							filetype pdb

							# The output pdb file

							output {0}.pdb

							structure {14}
							chain A
								resnumbers 3
								number {1:g}
								inside box 0. 0. {2}  {3} {4} {5}
								constrain_rotation x 180 10
								constrain_rotation y 180 10
								outside cylinder  {15} {16}  {19}  0.  0.  1.  {18}  {17}
							end structure

							structure {14}
								chain B
								resnumbers 3
								number {1:g}
								inside box 0. 0.  {8}  {3} {4} {9}
								constrain_rotation x 0 10
								constrain_rotation y 0 10
								outside cylinder  {15} {16}  {19}  0.  0.  1.  {18}  {17}
							end structure
							""".format(System, NLM[LipidType], M1headMIN, LXS, 
										LYS, M1tailMAX, M1headMAX, M1tailMIN, 
										M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
										NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType], 
										LXS/2.0, LYS/2.0, L_defo, radiusDefo, THICKNESS)
							
			PackmolInput += """
						
						structure {3}
							chain C
							resnumbers 3
							number {4:g}
							inside box 0. 0.  {5}  {0} {1} {2}
							constrain_rotation x 180 10
							constrain_rotation y 180 10
							outside cylinder  {8} {9}  {12}  0.  0.  1.  {11}  {10}
						end structure
						
						""".format(LXS, LYS, TMT+LZM, PDBfileList[LipidType], NBLIPIDS_MONO , LZM, 
									LXS/2.0, LYS/2.0, L_defo, radiusDefo, THICKNESS)
		
		#=======================================================================
		#=======================================================================
		#=======================================================================
		
		
						
		#=======================================================================
		# Setting the defo with solvent for packmol ============================
		#=======================================================================
		
		if SolventType == 'PW':
			PackmolInput += """
			
							structure {15}
								chain D
								number {12:g}
								inside box 0. 0. 0.  {3} {4} {2}
								atoms 2 3
									radius 0.2
								end atoms
							end structure


							structure {15}
								chain E
								number {12:g}
								inside box 0. 0. {9}  {3} {4} {13}
								atoms 2 3
									radius 0.2
								end atoms
							end structure
					
					""".format(System, NLM[LipidType], M1headMIN, LXS, 
								LYS, M1tailMAX, M1headMAX, M1tailMIN,
								M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
								NSOLM[SolventType], LZS, PDBfileList[SolventType])
		else:
			PackmolInput += """
						
						structure {14}
							chain D
							number {12:g}
							inside box 0. 0. {16}  {3} {4} {2}
						end structure
						
						structure {14}
							chain E
							number {12:g}
							inside box 0. 0. {9}  {3} {4} {13}
						end structure
						
						structure {17}
							chain X
							number 1
							resnumbers 3
							fixed {18} {19} {16} 0.0 0.0 0.0
							radius 0.
						end structure
						
						""".format(System, NLM[LipidType], M1headMIN, LXS, 
								LYS, M1tailMAX, M1headMAX, M1tailMIN,
								M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, 
								NSOLM[SolventType], LZM, PDBfileList[SolventType], M1headMIN, 
								THICKNESS, DefoXYZ_filename.replace('xyz','pdb'), 
								LXS/2.0, LYS/2.0, L_defo, radiusDefo)
						
		
		
		#=======================================================================
		# Adding the substrat ==================================================
		#=======================================================================
		
		PackmolInput += """
						
						structure {4}
							chain S
							number {3:g}
							inside box 0. 0. 0.  {0} {1} {2}
						end structure
						
						
						""".format(LXS, LYS, THICKNESS, nbSu, PDBfileList['SU'])
		
		
		f = open('packmol_'+System+'.input','w')
		f.write(Utility.RemoveUnwantedIndent(PackmolInput))
		f.close()
		
		# Lipids input pdb =====================================================
		if( LipidType == "DSPC"):
			f = open(PDBfileList['DSPC'],'w')
			f.write(Utility.RemoveUnwantedIndent(DSPC_PDB))
			f.close()
		if( LipidType == "DPPC"):
			f = open(PDBfileList['DPPC'],'w')
			f.write(Utility.RemoveUnwantedIndent(DPPC_PDB))
			f.close()
		if( LipidType == "DLPC"):
			f = open(PDBfileList['DLPC'],'w')
			f.write(Utility.RemoveUnwantedIndent(DLPC_PDB))
			f.close()
			
		# Solvents input pdb ===================================================
		if( SolventType == 'W'):
			f = open(PDBfileList['W'],'w')
			f.write(Utility.RemoveUnwantedIndent(W_PDB))
			f.close()
		if( SolventType == 'PW'):
			f = open(PDBfileList['PW'],'w')
			f.write(Utility.RemoveUnwantedIndent(PW_PDB))
			f.close()
		if( SolventType == 'OCO'):
			f = open(PDBfileList['OCO'],'w')
			f.write(Utility.RemoveUnwantedIndent(OCO_PDB))
			f.close()
			
		# pdb file for su
		suType = SU_TYPE
		if len(SU_TYPE) < 4:
			suType = SU_TYPE + (4 - len(SU_TYPE))*' '
		suPdb = SU_PDB.replace("TEMP", suType)
		f = open(PDBfileList['SU'],'w')
		f.write(Utility.RemoveUnwantedIndent(suPdb))
		f.close()
			
			
		#=======================================================================
		#lauching packmol
		#=======================================================================

		cmd = str("""{0} < packmol_{1}.input > packmol_{1}.output """
								).format(Softwares['PACKMOL'], System)
		sub.call(cmd, shell=True)

		#=======================================================================
		# ensure the right box in pdb file
		#=======================================================================

		WriteBox = str("""
				mol load pdb {0}.pdb
				set all [atomselect top "all"]

				package require pbctools
				pbc set {{{1} {2} {3}}}

				$all writepdb "{0}.withbox.pdb"
				unset all

				exit
				""").format(System, Sample['LX'], Sample['LY'], Sample['LZ'])

		f = open('write_box.vmd','w+')
		f.write(Utility.RemoveUnwantedIndent(WriteBox) )
		f.close()

		## ======================================================================
		cmd = str("""{0} -dispdev text -e write_box.vmd > write_box.log"""
												).format(Softwares['VMD'])
		sub.call(cmd, shell=True)
		
		MakeIndex = str("""
				chain A
				name 5 up{0}
				chain B
				name 6 low{0}
				chain C
				name 7 mono{0}
				chain D
				name 8 up{1}
				chain E
				name 9 low{1}
				chain S
				name 10 su
				chain X
				name 11 defo
				q
				
				""").format(LipidType, SolventType)

		f = open('make_index.input','w+')
		f.write(Utility.RemoveUnwantedIndent(MakeIndex) )
		f.close()
		
		cmd = str("""{0}make_ndx -f {1}.withbox.pdb -o {1}.ndx < make_index.input"""
											).format(GROMACS_LOC_prefixPath, System)
		sub.call(cmd, shell=True)
		
		
		#=======================================================================
		# the topology file
		#=======================================================================
		TopologyDefoSu(Sample, PathToDefault)
		
		Topology = """
						#include "martini_v2.2_{2}_{0}_DEFO_{1}.itp"
						#include "martini_v2.0_lipids.itp"
						
					""".format( Sample['SU']['Version'], Sample['DEFO']['Version'], SU_TYPE )
		
		#Copy the topology files for martini forcefield
		sub.call("""cp {0}/martini_v2.0_lipids.itp  .""".format(PathToDefault), shell= True)
		sub.call("""cp {0}/DEFO/defo_posres.itp  .""".format(PathToDefault), shell= True)
		sub.call("""cp {0}/SU/su_posres.itp  .""".format(PathToDefault), shell= True)
		f = open(System+'.top','w')
		f.write(Utility.RemoveUnwantedIndent(Topology))

		f = open(System+'.top','a')
		f.write("""\n[ system ]\n""")

		Topology = str("""{0}_{1}_WITH_DEFO_{2}_AND_{4}_{3}\n""").format(LipidType, Sample['TYPE'], Sample['DEFO']['Version'], Sample['SU']['Version'], SU_TYPE)
		f.write(Topology)

		f.write("""\n[ molecules ]\n""")
		Topology = str("""{0} {1}\n{2} {3}\n{4} {5}\n{6} {7}\n""").format(LipidType, Sample[LipidType]+NBLIPIDS_MONO,SolventType, Sample[SolventType],'DEFO', nbDefo, SU_TYPE, nbSu)
		f.write(Topology)
		f.close()
			
		#==================================================================================
		# Output the files for other steps
		#==================================================================================
		Output = str("""{0}.withbox.pdb""").format(System)
		Index = str("""{0}.ndx""").format(System)
		return { 'SYSTEM': System, 'OUTPUT': Output, 'INDEX':Index}


	################################################################################
	################################################################################
	################################################################################
	################################################################################


	else: #Default for Free Bilayer
		# packmol constraints are not strict !
		# put the molecules in a smaller box to
		# avoid initial crash because of PBC
		# the SHELL parameter defines the shell in which
		# packmol is not supposed to put particles
		SHELL = 3.0
		
		LXS = Sample['LX']-SHELL
		LYS = Sample['LY']-SHELL
		LZS = Sample['LZ']-SHELL

		LZ2 = LZS/2.0

		#Number of lipid and water per layer
		NLM = {}
		NSOLM = {}
		LipidType = ''
		
		for L in LipidsList:
			if(L in Sample):
				NLM.update( {L:int(Sample[L]/2)} )
				LipidType = L
		for Sol in SolventsList:
			print(Sol,' is in sample:', Sol in Sample)
			if Sol in Sample:
				print(Sol)
				NSOLM.update( {Sol:int(Sample[Sol]/2)} )
				SolventType = Sol
		
		#If the number of lipids per Monolayer is high
		# we cut the sample till we get a reasonnable amount
		# of lipis per monolayer for packmol
		NbMult = 0
		NeedToExpand = False
		while NLM[LipidType] > 512:
			NLM[LipidType] /= 2
			NSOLM[SolventType] /= 2
			NbMult += 1
			#diviser boîte
			NeedToExpand = True
			print(NLM[LipidType])
		print(LipidType)
		#==================================================================================
		# creating the initial bilayer (lipids + water) using packmol
		#==================================================================================

		System = str('{0}_{1}{2}_{3}{4}').format(Sample['TYPE'],Sample[LipidType], LipidType, Sample[SolventType], SolventType)
		
		#DSPC BILAYER
		if( LipidType == "DSPC"):
			# Geometry to preprare the bilayer with packmol

			# total monolayer thickness (Angstrom)
			TMT = 30.0

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 7.0

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
			
			# creating input for packmol
			PackmolInput = """
							#
							# Lipid bilayer with water, perpendicular to z axis
							#

							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.

							tolerance 3.0

							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)

							filetype pdb

							# The output pdb file

							output {0}.pdb

							structure {14}
								resnumbers 3
								number {1:g}
								inside box 0. 0. {2}  {3} {4} {5}
								atoms 1
									below plane 0. 0. 1. {6}
								end atoms
								atoms 9 14
									over plane 0. 0. 1. {7}
								end atoms
							end structure

							structure {14}
								resnumbers 3
								number {1:g}
								inside box 0. 0.  {8}  {3} {4} {9}
								atoms 1
									over plane 0. 0. 1. {10}
								end atoms
								atoms 9 14
									below plane 0. 0. 1. {11}
								end atoms
							end structure

							""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
			
			if SolventType == 'PW':
				PackmolInput += """
				
								structure {15}
									number {12:g}
									inside box 0. 0. 0.  {3} {4} {2}
									atoms 2 3
										radius 0.2
									end atoms
								end structure


								structure {15}
									number {12:g}
									inside box 0. 0. {9}  {3} {4} {13}
									atoms 2 3
										radius 0.2
									end atoms
								end structure
								
								""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
			else:
				PackmolInput += """
				
								structure {15}
									number {12:g}
									inside box 0. 0. 0.  {3} {4} {2}
								end structure


								structure {15}
									number {12:g}
									inside box 0. 0. {9}  {3} {4} {13}
								end structure
								
								""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
			
			f = open('packmol_'+System+'.input','w')
			f.write(Utility.RemoveUnwantedIndent(PackmolInput))
			f.close()
			
			f = open('dspc_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(DSPC_PDB))
			f.close()
		
		#DPPC BILAYER
		if( LipidType == "DPPC"):
			# Geometry to preprare the bilayer with packmol

			# total monolayer thickness (Angstrom)
			TMT = 30

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
			
			PackmolInput = """
							#
							# Lipid bilayer with water, perpendicular to z axis
							#

							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.

							tolerance 3.0

							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)

							filetype pdb

							# The output pdb file

							output {0}.pdb

							structure {14}
								resnumbers 3
								number {1:g}
								inside box 0. 0. {2}  {3} {4} {5}
								constrain_rotation x 180 10
								constrain_rotation y 180 10
							end structure

							structure {14}
								resnumbers 3
								number {1:g}
								inside box 0. 0.  {8}  {3} {4} {9}
								constrain_rotation x 0 10
								constrain_rotation y 0 10
							end structure

							""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
							
			if SolventType == 'PW':
				PackmolInput += """
				
								structure {15}
									number {12:g}
									inside box 0. 0. 0.  {3} {4} {2}
									atoms 2 3
										radius 0.2
									end atoms
								end structure


								structure {15}
									number {12:g}
									inside box 0. 0. {9}  {3} {4} {13}
									atoms 2 3
										radius 0.2
									end atoms
								end structure
								
								""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
			else:
				PackmolInput += """
				
								structure {15}
									number {12:g}
									inside box 0. 0. 0.  {3} {4} {2}
								end structure


								structure {15}
									number {12:g}
									inside box 0. 0. {9}  {3} {4} {13}
								end structure
								
								""".format(System, NLM[LipidType], M1headMIN, LXS, LYS, M1tailMAX, M1headMAX, M1tailMIN, M2tailMIN, M2headMAX, M2headMIN, M2tailMAX, NSOLM[SolventType], LZS, PDBfileList[LipidType], PDBfileList[SolventType])
			
			f = open('packmol_'+System+'.input','w')
			f.write(Utility.RemoveUnwantedIndent(PackmolInput))
			f.close()
			
			f = open('dppc_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(DPPC_PDB))
			f.close()
		
		#DLPC BILAYER
		if( LipidType == "DLPC"):
			# total monolayer thickness (Angstrom)
			TMT = 30

			# deltaz : thickness in Z direction for
			# the volume constraining the heads and tails beads
			DZ = 10

			M1headMIN = LZ2 - TMT
			M1headMAX = LZ2 - TMT + DZ
			M1tailMIN = LZ2 - DZ
			M1tailMAX = LZ2

			M2headMIN = LZ2 + TMT - DZ
			M2headMAX = LZ2 + TMT
			M2tailMIN = LZ2
			M2tailMAX = LZ2 + DZ
			
			PackmolInput = """
							#
							# Lipid bilayer with water, perpendicular to z axis
							#

							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.

							tolerance 3.0

							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)

							filetype pdb

							# The output pdb file

							output {0}.pdb

							structure {14}
								resnumbers 3
								number {1:g}
								inside box 0. 0. {2}  {3} {4} {5}
								constrain_rotation x 180 10
								constrain_rotation y 180 10
							end structure

							structure {14}
								resnumbers 3
								number {1:g}
								inside box 0. 0.  {8}  {3} {4} {9}
								constrain_rotation x 0 10
								constrain_rotation y 0 10
							end structure
							""".format(System, NLM[LipidType], M1headMIN, LXS, 
										LYS, M1tailMAX, M1headMAX, M1tailMIN, 
										M2tailMIN, M2headMAX, M2headMIN, 
										M2tailMAX, NSOLM[SolventType], LZS, 
										PDBfileList[LipidType], 
										PDBfileList[SolventType])

			if SolventType == 'PW':
				PackmolInput += """
				
								structure {15}
									number {12:g}
									inside box 0. 0. 0.  {3} {4} {2}
									atoms 2 3
										radius 0.2
									end atoms
								end structure


								structure {15}
									number {12:g}
									inside box 0. 0. {9}  {3} {4} {13}
									atoms 2 3
										radius 0.2
									end atoms
								end structure
								
								""".format(System, NLM[LipidType], M1headMIN, 
											LXS,LYS, M1tailMAX, M1headMAX, 
											M1tailMIN, M2tailMIN,M2headMAX, 
											M2headMIN,M2tailMAX, 
											NSOLM[SolventType],LZS, 
											PDBfileList[LipidType], 
											PDBfileList[SolventType])
			else:
				PackmolInput += """
				
								structure {15}
									number {12:g}
									inside box 0. 0. 0.  {3} {4} {2}
								end structure


								structure {15}
									number {12:g}
									inside box 0. 0. {9}  {3} {4} {13}
								end structure
								
								""".format(System, NLM[LipidType],
											M1headMIN,LXS, LYS, M1tailMAX, 
											M1headMAX, M1tailMIN, M2tailMIN, 
											M2headMAX, M2headMIN, M2tailMAX, 
											NSOLM[SolventType], LZS, 
											PDBfileList[LipidType], 
											PDBfileList[SolventType])
			
			f = open('packmol_'+System+'.input','w')
			f.write(Utility.RemoveUnwantedIndent(PackmolInput))
			f.close()
			
			f = open('dlpc_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(DLPC_PDB))
			f.close()
		
		# water input pdb
		if( SolventType == 'W'):
			f = open('water_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(W_PDB))
			f.close()
		if( SolventType == 'OCO'):
			f = open('octanol_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(OCO_PDB))
			f.close()
		if( SolventType == 'PW'):
			f = open('polwater_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(PW_PDB))
			f.close()
		

#===============================================================================
		#lauching packmol
#===============================================================================

		cmd = str("""{0} < packmol_{1}.input > packmol_{1}.output """
					).format(Softwares['PACKMOL'],System)
		sub.call(cmd, shell=True)

		
#===============================================================================
		# ensure the right box in pdb file
#===============================================================================

		WriteBox = str("""
				mol load pdb {0}.pdb
				set all [atomselect top "all"]

				package require pbctools
				pbc set {{{1} {2} {3}}}

				$all writepdb "{0}.withbox.pdb"
				unset all

				exit
				""").format(System, Sample['LX'], Sample['LY'], Sample['LZ'])

		f = open('write_box.vmd','w+')
		f.write(Utility.RemoveUnwantedIndent(WriteBox) )
		f.close()

		## ======================================================================
		cmd = str("""{0} -dispdev text -e write_box.vmd > write_box.log""" 
					).format(Softwares['VMD'])
		sub.call(cmd, shell=True)

		
#===============================================================================
		# For big samples
#===============================================================================
		if NeedToExpand:
			cmd = str("""{0}genconf -f {1}.withbox.pdb -nbox {2} {2} 1 -o {1}.withbox.pdb""").format(GROMACS_LOC_prefixPath, System, NbMult)
			sub.call(cmd, shell=True)
		## ======================================================================
		ApL = Sample['LX']*Sample['LY']/NLM[LipidType]
		print(Utility.RemoveUnwantedIndent(str("""
				================================
				================================
				Packmol finished initial input file
				{0} {1}, {2} {3}
				box sizes : {4}, {5}, {6}
				Area per lipid = {7} A**2
				===============================
				===============================
				""").format(LipidType, Sample[LipidType],SolventType, Sample[SolventType], Sample['LX'],Sample['LY'],Sample['LZ'],ApL)))

		#==================================================================================
		# the topology file
		#==================================================================================

		Topology = str("""
					#include "martini_v2.2.itp" ; modified with polarisable water
					#include "martini_v2.0_lipids.itp"
					""")
		#Copy the topology files for martini forcefield
		sub.call("""cp {0}/martini_v2.0_lipids.itp {0}/martini_v2.2.itp ./""".format(PathToDefault), shell= True)
		f = open(System+'.top','w')
		f.write(Utility.RemoveUnwantedIndent(Topology))

		f = open(System+'.top','a')
		f.write("""\n[ system ]\n""")

		Topology = str("""{0} {1}\n""").format(LipidType, Sample['TYPE'])
		f.write(Topology)

		###add a for loop for multiple types (Later)
		f.write("""\n[ molecules ]\n""")
		Topology = str("""{0} {1}\n{2} {3}""").format(LipidType, Sample[LipidType],SolventType, Sample[SolventType])
		f.write(Topology)
		f.close()

		#==================================================================================
		# the index file
		#==================================================================================

		cmd = str("""echo q | {0}make_ndx -f {1}.withbox.pdb -o {1}.ndx""").format(GROMACS_LOC_prefixPath,System)
		sub.call(cmd, shell=True)

		#==================================================================================
		# Output the files for other steps
		#==================================================================================
		Output = str("""{0}.withbox.pdb""").format(System)
		Index = str("""{0}.ndx""").format(System)
		return { 'SYSTEM': System, 'OUTPUT': Output, 'INDEX':Index}





def TopologyDefoSu(Sample, PathToDefault):
	Headings = ["atomtypes","nonbond_params","moleculetype","atoms"]
	IsuTopology = {}
	IdefoTopology = {}
	DefoAtomtype = ""
	DefoNonBondParams = ""
	DefoMolType = ""
	DefoAtoms = ""
	
	IncludeSuTopologyFile = PathToDefault+"""/SU/SU_{0}.itp""".format(Sample['SU']['Version'])
	
	IncludeDefoTopologyFile = PathToDefault+"""/DEFO/DEFO_{0}.itp""".format(Sample['DEFO']['Version'])
	
	with open(IncludeSuTopologyFile,'r') as ITPSu:
		for Head in Headings:
			for heading_and_lines in Utility.group_by_heading(ITPSu, Head):
				lines = []
				if Head is not 'moleculetype':
					if Head is not 'atoms':
						lines.extend([';;;;;;; SU_{0}\n'.format(Sample['SU']['Version'])])
				lines.extend(heading_and_lines[2:])
				IsuTopology.update({Head:''.join(lines)})
	
	PosResSu = Utility.RemoveUnwantedIndent("""
										#ifdef SU_POSRES
										#include "su_posres.itp"
										#endif
										
										""")
	
	if '[ moleculetype ]' in IsuTopology['moleculetype'] or '[moleculetype]' in IsuTopology['moleculetype']:
		IsuTopology['moleculetype'] = IsuTopology['moleculetype'].replace('[ moleculetype ]', PosResSu+'[ moleculetype ]' )
	IsuTopology['moleculetype'] = '[ moleculetype ]\n'+IsuTopology['moleculetype']+'\n'+PosResSu
			
		
	with open(IncludeDefoTopologyFile,'r') as ITPDefo:
		for Head in Headings:
			for heading_and_lines in Utility.group_by_heading(ITPDefo, Head):
				lines = []
				if Head is not 'moleculetype':
					if Head is not 'atoms':
						lines.extend([';;;;;;; SU_{0}\n'.format(Sample['DEFO']['Version'])])
				lines.extend(heading_and_lines[2:])
				IdefoTopology.update({Head:''.join(lines)})
	
	if os.path.isfile("""martini_v2.2_{2}_{0}_DEFO_{1}.itp""".format(Sample['SU']['Version'], Sample['DEFO']['Version'],Sample['SU']['SuType'])):
		os.remove("""martini_v2.2_{2}_{0}_DEFO_{1}.itp""".format(Sample['SU']['Version'], Sample['DEFO']['Version'], Sample['SU']['SuType']))
	
	TempOut = ''
	
	Output = open("""martini_v2.2_{2}_{0}_DEFO_{1}.itp""".format(Sample['SU']['Version'], Sample['DEFO']['Version'], Sample['SU']['SuType']),'a+')
	
	with open(PathToDefault+"""/martini_v2.2.itp""",'r') as DefMartini:
		
		for line in DefMartini:
			if 'nonbond_params' in line:
				TempOut += IsuTopology['atomtypes']
				TempOut += '\n'
			if 'PLACE_FOR_SU' in line:
				TempOut += IsuTopology['nonbond_params']
				TempOut += '\n'
			else:
				TempOut += line
		
		
		for line in TempOut.splitlines():
			if 'nonbond_params' in line:
				Output.write(IdefoTopology['atomtypes'])
				Output.write('\n')
			if 'PLACE_FOR_DEFO' in line:
				Output.write(IdefoTopology['nonbond_params'])
				Output.write('\n')
			else:
				Output.write(line)
				Output.write('\n')
	
	
	Output.write("\n;;;;;;; DEFO_{0}\n".format(Sample['DEFO']['Version']))
	Output.write("[ moleculetype ]\n"+IdefoTopology['moleculetype']+'\n')
	Output.write("[ atoms ]\n"+IdefoTopology['atoms'])
	Output.write(Utility.RemoveUnwantedIndent("""
		
											#ifdef DEFO_POSRES
											#include "defo_posres.itp"
											#endif
											
											"""))
	
	Output.write("\n;;;;;;; SU_{0}\n".format(Sample['SU']['Version']))
	Output.write(IsuTopology['moleculetype']+'\n')
	Output.close()


def TopologyDefo(Sample, PathToDefault):
	Headings = ["atomtypes","nonbond_params","moleculetype","atoms"]
	Itopology = {}
	DefoAtomtype = ""
	DefoNonBondParams = ""
	DefoMolType = ""
	DefoAtoms = ""
	
	IncludeTopologyFile = PathToDefault+"""/DEFO/DEFO_{0}.itp""".format(Sample['DEFO']['Version'])
	
	with open(IncludeTopologyFile,'r') as ITPDefo:
		for Head in Headings:
			for heading_and_lines in Utility.group_by_heading( ITPDefo, Head):
				lines = []
				if Head is not 'moleculetype':
					if Head is not 'atoms':
						lines.extend([';;;;;;; DEFO_{0}\n'.format(Sample['DEFO']['Version'])])
				lines.extend(heading_and_lines[2:])
				Itopology.update({Head:''.join(lines)})
	
	if os.path.isfile("""martini_v2.2_DEFO_{0}.itp""".format(Sample['DEFO']['Version'])):
		os.remove("""martini_v2.2_DEFO_v{0}.itp""".format(Sample['DEFO']['Version']))
			
	Output = open("""martini_v2.2_DEFO_{0}.itp""".format(Sample['DEFO']['Version']),'a')
	with open(PathToDefault+"""/martini_v2.2.itp""",'r') as DefMartini:
		
		for line in DefMartini:
			if 'nonbond_params' in line:
				Output.write(Itopology['atomtypes'])
				#Output.write('[ nonbond_params ]')
			if 'PLACE_FOR_DEFO' in line:
				Output.write(Itopology['nonbond_params'])
				Output.write('')
			else:
				Output.write(line)
		
	Output.write(";;;;;;; DEFO_{0}\n".format(Sample['DEFO']['Version']))
	Output.write("[ moleculetype ]\n"+Itopology['moleculetype']+'\n')
	Output.write("[ atoms ]\n"+Itopology['atoms'])
	Output.write(Utility.RemoveUnwantedIndent("""
											#ifdef DEFO_POSRES
											#include "defo_posres.itp"
											#endif
											"""))
	Output.close()


def TopologySu(Sample, PathToDefault):
	Headings = ["atomtypes","nonbond_params","moleculetype","atoms"]
	IsuTopology = {}
	DefoAtomtype = ""
	DefoNonBondParams = ""
	DefoMolType = ""
	DefoAtoms = ""
	
	IncludeSuTopologyFile = PathToDefault+"""/SU/SU_{0}.itp""".format(Sample['SU']['Version'])
	
	with open(IncludeSuTopologyFile,'r') as ITPSu:
		for Head in Headings:
			for heading_and_lines in Utility.group_by_heading( ITPSu, Head):
				lines = []
				if Head is not 'moleculetype':
					if Head is not 'atoms':
						lines.extend([';;;;;;; SU_{0}\n'.format(Sample['SU']['Version'])])
				lines.extend(heading_and_lines[2:])
				IsuTopology.update({Head:''.join(lines)})
	
	PosResSu = Utility.RemoveUnwantedIndent("""
										#ifdef SU_POSRES
										#include "su_posres.itp"
										#endif
										
										""")
	
	if '[ moleculetype ]' in IsuTopology['moleculetype'] or '[moleculetype]' in IsuTopology['moleculetype']:
		IsuTopology['moleculetype'] = IsuTopology['moleculetype'].replace('[ moleculetype ]', PosResSu+'[ moleculetype ]' )
	IsuTopology['moleculetype'] = '[ moleculetype ]\n'+IsuTopology['moleculetype']+'\n'+PosResSu
	
	if os.path.isfile("""martini_v2.2_{1}_{0}.itp""".format(Sample['SU']['Version'], Sample['SU']['SuType'])):
		os.remove(""""martini_v2.2_{1}_{0}.itp""".format(Sample['SU']['Version'], Sample['SU']['SuType']))
			
	Output = open("""martini_v2.2_{1}_{0}.itp""".format(Sample['SU']['Version'], Sample['SU']['SuType']),'a')
	with open(PathToDefault+"""/martini_v2.2.itp""",'r') as DefMartini:
		
		for line in DefMartini:
			if 'nonbond_params' in line:
				Output.write(IsuTopology['atomtypes'])
				#Output.write('[ nonbond_params ]')
			if 'PLACE_FOR_SU' in line:
				Output.write(IsuTopology['nonbond_params'])
				Output.write('')
			else:
				Output.write(line)
		
	Output.write(";;;;;;; SU_{0}\n".format(Sample['SU']['Version']))
	Output.write(IsuTopology['moleculetype']+'\n')
	Output.close()



def InitSolvent(Sample, Softwares, GROMACS_LOC_prefixPath, PathToDefault):
	# packmol constraints are not strict !
	# put the molecules in a smaller box to
	# avoid initial crash because of PBC
	# the SHELL parameter defines the shell in which
	# packmol is not supposed to put particles
	
	
	SHELL = 3.0
	
	LXS = 0.0
	LYS = 0.0
	LZS = 0.0
	
	if 'FILLMODE' in Sample:
		if Sample['FILLMODE'] == 'FULL':
			LXS = Sample['LX']-SHELL
			LYS = Sample['LY']-SHELL
			LZS = Sample['LZ']-SHELL
		if Sample['FILLMODE'] == 'BOX':
			LXS = LYS = LZS = Sample['LX']-SHELL
		if Sample['FILLMODE'] == 'HALF-X':
			LXS = Sample['LX']/2.0-SHELL
			LYS = Sample['LY']-SHELL
			LZS = Sample['LZ']-SHELL
		if Sample['FILLMODE'] == 'HALF-Y':
			LXS = Sample['LX']-SHELL
			LYS = Sample['LY']/2.0-SHELL
			LZS = Sample['LZ']-SHELL
		if Sample['FILLMODE'] == 'HALF-Z':
			LXS = Sample['LX']-SHELL
			LYS = Sample['LY']-SHELL
			LZS = Sample['LZ']/2.0-SHELL
	else:
		LXS = Sample['LX']-SHELL
		LYS = Sample['LY']-SHELL
		LZS = Sample['LZ']-SHELL
	
	Solvents = []
	NbSol = 0
	for Sol in SolventsList:
		if(Sol in Sample):
			Solvents.append(Sol)
			NbSol += 1
			
	#==================================================================================
	# Only one solvent case
	#==================================================================================
	if NbSol == 1:
		SolventType = Solvents[0]
		#==================================================================================
		# creating the initial bilayer (lipids + water) using packmol
		#==================================================================================
		
		System = str('{0}_{1}{2}').format(Sample['TYPE'], Sample[SolventType], SolventType)
		if SolventType == 'PW':
			# creating input for packmol
			PackmolInput = str("""
							#
							#  solvent
							#
							
							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.
							
							tolerance 3.0
							
							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)
							
							filetype pdb
							
							# The output pdb file
							
							output {0}.pdb
							
							structure {5}
								number {1:g}
								inside box 0. 0. 0.  {2} {3} {4}
								atoms 2 3
									radius 0.2
								end atoms
							end structure
							""").format(System, Sample[SolventType], LXS, LYS, LZS, PDBfileList[SolventType])
			
			f = open('packmol_'+System+'.input','w')
			f.write(Utility.RemoveUnwantedIndent(PackmolInput))
			f.close()
		else:
			# creating input for packmol
			PackmolInput = str("""
							#
							#  solvent
							#
							
							# Every atom from diferent molecules will be far from each other at
							# least 3.0 Anstroms at the solution.
							
							tolerance 3.0
							
							# Coordinate file types will be in pdb format (keyword not required for
							# pdb file format, but required for tinker, xyz or moldy)
							
							filetype pdb
							
							# The output pdb file
							
							output {0}.pdb
							
							structure {5}
								number {1:g}
								inside box 0. 0. 0.  {2} {3} {4}
							end structure
							""").format(System, Sample[SolventType], LXS, LYS, LZS, PDBfileList[SolventType])
			
			f = open('packmol_'+System+'.input','w')
			f.write(Utility.RemoveUnwantedIndent(PackmolInput))
			f.close()
		
		# water input pdb
		if( SolventType == 'W'):
			f = open('water_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(W_PDB))
			f.close()
		
		if( SolventType == 'OCO'):
			f = open('octanol_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(OCO_PDB))
			f.close()
		
		if( SolventType == 'PW'):
			f = open('polwater_single.pdb','w')
			f.write(Utility.RemoveUnwantedIndent(PW_PDB))
			f.close()

		
		#==================================================================================
		#lauching packmol
		#==================================================================================
		
		cmd = str("""{0} < packmol_{1}.input > packmol_{1}.output """).format(Softwares['PACKMOL'],System)
		sub.call(cmd, shell=True)
		
		#==================================================================================
		# ensure the right box in pdb file
		#==================================================================================
		
		WriteBox = str("""
				mol load pdb {0}.pdb
				set all [atomselect top "all"]
		
				package require pbctools
				pbc set {{{1} {2} {3}}}
				
				$all writepdb "{0}.withbox.pdb"
				unset all
				
				exit
				""").format(System, Sample['LX'], Sample['LY'], Sample['LZ'])
		
		f = open('write_box.vmd','w+')
		f.write(Utility.RemoveUnwantedIndent(WriteBox) )
		f.close()
		
		## ======================================================================
		cmd = str("""{0} -dispdev text -e write_box.vmd > write_box.log""").format(Softwares['VMD'])
		sub.call(cmd, shell=True)
		
		## ======================================================================
		print(Utility.RemoveUnwantedIndent(str("""
				================================
				================================
				Packmol finished initial input file
				{0} {1}
				box sizes : {2}, {3}, {4}
				===============================
				===============================
				""").format(SolventType, Sample[SolventType], Sample['LX'],Sample['LY'],Sample['LZ']) ))
		
		#==================================================================================
		# the topology file
		#==================================================================================
		
		Topology = str("""
					#include "martini_v2.2.itp" ; modified with polarisable water
					#include "martini_v2.0_solvents.itp"
					""")
		#Copy the topology files for martini forcefield
		sub.call("""cp {0}/martini_v2.0_solvents.itp {0}/martini_v2.2.itp ./""".format(PathToDefault), shell= True)
		f = open(System+'.top','w')
		f.write(Utility.RemoveUnwantedIndent(Topology))
		
		f = open(System+'.top','a')
		f.write(Utility.RemoveUnwantedIndent("""
						
						[ system ]
						{0}
						
						""".format(System)))
		
		###add a for loop for multiple types (Later)
		f.write("""\n[ molecules ]\n""")
		Topology = str("""{0} {1}""").format(SolventType, Sample[SolventType])
		f.write(Topology)
		f.close()
		
		#==================================================================================
		# the index file
		#==================================================================================
		cmd = str("""echo q | {0}make_ndx -f {1}.withbox.pdb -o {1}.ndx""").format(GROMACS_LOC_prefixPath,System)
		sub.call(cmd, shell=True)
		
		#==================================================================================
		# Output the files for other steps
		#==================================================================================
		Output = str("""{0}.withbox.pdb""").format(System)
		Index = str("""{0}.ndx""").format(System)
		return { 'SYSTEM': System, 'OUTPUT': Output, 'INDEX':Index}
	
	#==================================================================================
	# More than one solvent case
	#==================================================================================
	if NbSol > 1:
		#==================================================================================
		# creating the initial bilayer (lipids + water) using packmol
		#==================================================================================
		Qt = ''
		for Sol in Solvents:
			Qt += "{0}{1}_".format(Sample[Sol], Sol)
		#Remove last underscore
		li = Qt.rsplit('_',1)
		Qt = ('').join(li)
		#**********************
		System = str('{0}_{1}').format(Sample['TYPE'], Qt)
		
		# creating input for packmol
		f = open('packmol_'+System+'.input','a+')
		PackmolInput = str("""
						#
						#  solvent
						#
						
						# Every atom from diferent molecules will be far from each other at
						# least 3.0 Anstroms at the solution.
						
						tolerance 3.0
						
						# Coordinate file types will be in pdb format (keyword not required for
						# pdb file format, but required for tinker, xyz or moldy)
						
						filetype pdb
						
						# The output pdb file
						
						output {0}.pdb
						
						
						""").format(System)
		f.write(Utility.RemoveUnwantedIndent(PackmolInput))
		Shift = 0.
		for Sol in Solvents:
			print(Sol)
			if Sol == 'PW':
				PackmolInput = str("""
						
						structure {5}
							resnumbers 3
							number {0:g}
							inside box 0. 0. {4} {1} {2} {3}
							atoms 2 3
								radius 0.2
							end atoms
						end structure
						
						""").format(Sample[Sol], LXS, LYS, (LZS/NbSol)+Shift, Shift, PDBfileList[Sol])
				f.write(Utility.RemoveUnwantedIndent(PackmolInput))
			else:
				PackmolInput = str("""
						
						structure {5}
							resnumbers 3
							number {0:g}
							inside box 0. 0. {4} {1} {2} {3}
						end structure
						
						""").format(Sample[Sol], LXS, LYS, (LZS/NbSol)+Shift, Shift, PDBfileList[Sol])
				f.write(Utility.RemoveUnwantedIndent(PackmolInput))
				Shift += LZS/NbSol
				
		f.close()
		
		for Sol in Solvents:
			if( Sol == 'W'):
				f = open('water_single.pdb','w')
				f.write(Utility.RemoveUnwantedIndent(W_PDB))
				f.close()
		
			if( Sol == 'OCO'):
				f = open('octanol_single.pdb','w')
				f.write(Utility.RemoveUnwantedIndent(OCO_PDB))
				f.close()
			
			if( Sol == 'PW'):
				f = open('polwater_single.pdb','w')
				f.write(Utility.RemoveUnwantedIndent(PW_PDB))
				f.close()
		
		
		#==================================================================================
		#lauching packmol
		#==================================================================================
		
		cmd = str("""{0} < packmol_{1}.input > packmol_{1}.output """).format(Softwares['PACKMOL'],System)
		sub.call(cmd, shell=True)
		
		#==================================================================================
		# ensure the right box in pdb file
		#==================================================================================
		
		WriteBox = str("""
				mol load pdb {0}.pdb
				set all [atomselect top "all"]
		
				package require pbctools
				pbc set {{{1} {2} {3}}}
				
				$all writepdb "{0}.withbox.pdb"
				unset all
				
				exit
				""").format(System, Sample['LX'], Sample['LY'], Sample['LZ'])
		
		f = open('write_box.vmd','w+')
		f.write(Utility.RemoveUnwantedIndent(WriteBox) )
		f.close()
		
		## ======================================================================
		cmd = str("""{0} -dispdev text -e write_box.vmd > write_box.log""").format(Softwares['VMD'])
		sub.call(cmd, shell=True)
		
		## ======================================================================
		print(Utility.RemoveUnwantedIndent("""
				================================
				================================
				Packmol finished initial input file"""))
		for Sol in Solvents:
			print("""{0} {1}""".format(Sol, Sample[Sol]))
		print(Utility.RemoveUnwantedIndent("""
				box sizes : {0}, {1}, {2}
				===============================
				===============================
				""").format(Sample['LX'],Sample['LY'],Sample['LZ']) )
		
		#==================================================================================
		# the topology file
		#==================================================================================
		
		Topology = str("""
					#include "martini_v2.2.itp" ; modified with polarisable water
					#include "martini_v2.0_solvents.itp"
					""")
		#Copy the topology files for martini forcefield
		sub.call("""cp {0}/martini_v2.0_solvents.itp {0}/martini_v2.2.itp ./""".format(PathToDefault), shell= True)
		f = open(System+'.top','w')
		f.write(Utility.RemoveUnwantedIndent(Topology))
		
		f = open(System+'.top','a')
		f.write(Utility.RemoveUnwantedIndent("""
						
						[ system ]
						{0}
						
						""".format(System)))
		
		f.write("""\n[ molecules ]\n""")
		for Sol in Solvents:
			Topology = str("""{0} {1} \n""").format(Sol, Sample[Sol])
			f.write(Topology)
		f.close()
		
		#==================================================================================
		# the index file
		#==================================================================================
		cmd = str("""echo q | {0}make_ndx -f {1}.withbox.pdb -o {1}.ndx""").format(GROMACS_LOC_prefixPath,System)
		sub.call(cmd, shell=True)
		
		#==================================================================================
		# Output the files for other steps
		#==================================================================================
		Output = str("""{0}.withbox.pdb""").format(System)
		Index = str("""{0}.ndx""").format(System)
		return { 'SYSTEM': System, 'OUTPUT': Output, 'INDEX':Index}



















def CopySample(Jobs, currentJob, step, PathToDefault):
	
	SampleToCopy = Jobs[ currentJob['PROTOCOL'][step]['samplenumber'] ]
	SampleToCopyName = Jobs[ currentJob['PROTOCOL'][step]['samplenumber'] ]['JOBID']
	currentJobName = currentJob['JOBID']
	
	copyMethod = currentJob['PROTOCOL'][step]['method']
	
	PDBfilepath = glob.glob('../'+SampleToCopyName+'/*.withbox.pdb')[0]
	TOPfilepath = glob.glob('../'+SampleToCopyName+'/*.top')[0]
	NDXfilepath = glob.glob('../'+SampleToCopyName+'/*.ndx')[0]
	
	if copyMethod:
		if copyMethod == "structure":
			if 'DEFO' in SampleToCopy or 'DEFO' in currentJob:
				if not ('DEFO' in SampleToCopy and 'DEFO' in currentJob):
					if 'SU' in SampleToCopy:
						print("DEFO is in {0} but not in {1} while using structure copy method.".format(SampleToCopyName, currentJobName))
					else:
						print("DEFO is in {0} but not in {1} while using structure copy method.".format(currentJobName, SampleToCopyName))
					return -1
				
			if 'SU' in SampleToCopy or 'SU' in currentJob:
				if not ('SU' in SampleToCopy and 'SU' in currentJob):
					if 'SU' in SampleToCopy:
						print("SU is in {0} but not in {1} while using structure copy method.".format(SampleToCopyName, currentJobName))
					else:
						print("SU is in {0} but not in {1} while using structure copy method.".format(currentJobName, SampleToCopyName))
					return -1
			
			if 'DEFO' in currentJob and 'SU' in currentJob:
				defoVersionBefore = SampleToCopy['DEFO']['Version']
				defoVersionCurrent = currentJob['DEFO']['Version']
				
				suVersionBefore = SampleToCopy['SU']['Version']
				suTypeBefore = SampleToCopy['SU']['SuType']
				
				suVersionCurrent = currentJob['SU']['Version']
				suTypeCurrent = currentJob['SU']['SuType']
				
				#Add columns for pdb format
				nbCols = len(suTypeBefore) - len(suTypeCurrent)
				if nbCols < 0:
					suTypeBefore += (-nbCols)*' '
				elif nbCols > 0:
					suTypeCurrent += nbCols*' '
					
				# If copy pdb file when modifying SuType, the pdb file should be changed with the correct SuType
				# The name should also be changed with the correct version and SuType, the number of SU being the same
				
				PDBfile = open(PDBfilepath,'r')
				PDBfileCurrent = PDBfile.read().replace(suTypeBefore, suTypeCurrent)
				PDBfile.close()
				
				
				PDBfilenameBefore = PDBfilepath.split('/')[-1]
				
				fixedPart = PDBfilenameBefore.split('_')[:-3]
				defoPart = PDBfilenameBefore.split('_')[-2]
				suPart = PDBfilenameBefore.split('_')[-1]
				
				suPart = suPart.replace(suTypeBefore.strip(' '), suTypeCurrent.strip(' '))
				suPart = suPart.replace(suVersionBefore, suVersionCurrent)
				
				defoPart = defoPart.replace(defoVersionBefore, defoVersionCurrent)
				
				PDBfilenameCurrent = fixedPart
				PDBfilenameCurrent.extend([defoPart, suPart])
				PDBfilenameCurrent = '_'.join(PDBfilenameCurrent)
				
				PDBfile = open(PDBfilenameCurrent, 'w')
				PDBfile.write(PDBfileCurrent)
				PDBfile.close()
				
				#Topology ##########################################################
				TOPfile = open(TOPfilepath, 'r')
				
				suTypeNVersionBefore = suTypeBefore+'_'+suVersionBefore
				suTypeNVersionCurrent = suTypeCurrent.strip(' ')+'_'+suVersionCurrent
				
				defoTypeNVersionBefore = 'DEFO_'+defoVersionBefore
				defoTypeNVersionCurrent = 'DEFO_'+defoVersionCurrent
				
				#Replacing for new .top file
				#For headers and [system]
				TOPfileCurrent = TOPfile.read().replace(suTypeNVersionBefore, suTypeNVersionCurrent)
				
				TOPfileCurrent = TOPfileCurrent.replace(defoTypeNVersionBefore, defoTypeNVersionCurrent)
				
				#For [molecules]
				TOPfileCurrent = TOPfileCurrent.replace(suTypeBefore, suTypeCurrent.strip(' '))
				
				TOPfile.close()
				TOPfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.top')
				TOPfile = open(TOPfilenameCurrent,'w')
				TOPfile.write(TOPfileCurrent)
				TOPfile.close()
				
				#Topology ITP ##########################################################
				TopologyDefoSu(currentJob, PathToDefault)
				
				#Index #########################################################
				NDXfile = open(NDXfilepath,'r')
				NDXfileCurrent = NDXfile.read()
				NDXfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.ndx')
				NDXfile.close()
				
				NDXfile = open(NDXfilenameCurrent,'w')
				NDXfile.write(NDXfileCurrent)
				NDXfile.close()
				
				#POSRES ########################################################
				sub.call('cp ../'+SampleToCopyName+'/*posres.itp .', shell= True)
			
			
			elif 'DEFO' not in currentJob and 'SU' in currentJob:
				suVersionBefore = SampleToCopy['SU']['Version']
				suTypeBefore = SampleToCopy['SU']['SuType']
				
				suVersionCurrent = currentJob['SU']['Version']
				suTypeCurrent = currentJob['SU']['SuType']
				
				#Add columns for pdb format
				nbCols = len(suTypeBefore) - len(suTypeCurrent)
				if nbCols < 0:
					suTypeBefore += (-nbCols)*' '
				elif nbCols > 0:
					suTypeCurrent += nbCols*' '
				
				PDBfile = open(PDBfilepath,'r')
				PDBfileCurrent = PDBfile.read().replace(suTypeBefore, suTypeCurrent)
				PDBfile.close()
				
				PDBfilenameBefore = PDBfilepath.split('/')[-1]
				
				fixedPart = PDBfilenameBefore.split('_')[:-2]
				suPart = PDBfilenameBefore.split('_')[-1]
				
				suPart = suPart.replace(suTypeBefore.strip(' '), suTypeCurrent.strip(' '))
				suPart = suPart.replace(suVersionBefore, suVersionCurrent)
				
				PDBfilenameCurrent = fixedPart
				PDBfilenameCurrent.append(suPart)
				PDBfilenameCurrent = '_'.join(PDBfilenameCurrent)
				
				PDBfile = open(PDBfilenameCurrent, 'w')
				PDBfile.write(PDBfileCurrent)
				PDBfile.close()
				
				#Topology ##########################################################
				TOPfile = open(TOPfilepath, 'r')
				
				suTypeNVersionBefore = suTypeBefore.strip(' ')+'_'+suVersionBefore
				suTypeNVersionCurrent = suTypeCurrent.strip(' ')+'_'+suVersionCurrent
				
				#Replacing for new .top file
				#For headers and [system]
				TOPfileCurrent = TOPfile.read().replace(suTypeNVersionBefore, suTypeNVersionCurrent)
				
				#For [molecules]
				TOPfileCurrent = TOPfileCurrent.replace(suTypeBefore, suTypeCurrent.strip(' '))
				
				TOPfile.close()
				TOPfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.top')
				TOPfile = open(TOPfilenameCurrent,'w')
				TOPfile.write(TOPfileCurrent)
				TOPfile.close()
				
				#Topology ITP ##########################################################
				TopologySu(currentJob, PathToDefault)
				
				#Index #########################################################
				NDXfile = open(NDXfilepath,'r')
				NDXfileCurrent = NDXfile.read()
				NDXfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.ndx')
				NDXfile.close()
				
				NDXfile = open(NDXfilenameCurrent,'w')
				NDXfile.write(NDXfileCurrent)
				NDXfile.close()
				
				#POSRES ########################################################
				sub.call('cp ../'+SampleToCopyName+'/*posres.itp .', shell= True)
			
			
			elif 'DEFO' in currentJob and 'SU' not in currentJob:
				defoVersionBefore = SampleToCopy['DEFO']['Version']
				defoVersionCurrent = currentJob['DEFO']['Version']
				
				# If copy pdb file when modifying SuType, the pdb file should be changed with the correct SuType
				# The name should also be changed with the correct version and SuType, the number of SU being the same
				
				PDBfile = open(PDBfilepath,'r')
				PDBfileCurrent = PDBfile.read()
				PDBfile.close()
				
				
				PDBfilenameBefore = PDBfilepath.split('/')[-1]
				
				fixedPart = PDBfilenameBefore.split('_')[:-2]
				defoPart = PDBfilenameBefore.split('_')[-1]
				
				defoPart = defoPart.replace(defoVersionBefore, defoVersionCurrent)
				
				PDBfilenameCurrent = fixedPart
				PDBfilenameCurrent.append(defoPart)
				PDBfilenameCurrent = '_'.join(PDBfilenameCurrent)
				
				PDBfile = open(PDBfilenameCurrent, 'w')
				PDBfile.write(PDBfileCurrent)
				PDBfile.close()
				
				#Topology ##########################################################
				TOPfile = open(TOPfilepath, 'r')
				
				defoTypeNVersionBefore = 'DEFO_'+defoVersionBefore
				defoTypeNVersionCurrent = 'DEFO_'+defoVersionCurrent
				
				#Replacing for new .top file
				#For headers and [system]
				TOPfileCurrent = TOPfile.read().replace(defoTypeNVersionBefore, defoTypeNVersionCurrent)
				
				TOPfile.close()
				TOPfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.top')
				
				TOPfile = open(TOPfilenameCurrent,'w')
				TOPfile.write(TOPfileCurrent)
				TOPfile.close()
				
				#Topology ITP ##########################################################
				TopologyDefo(currentJob, PathToDefault)
				
				#Index #########################################################
				NDXfile = open(NDXfilepath,'r')
				NDXfileCurrent = NDXfile.read()
				NDXfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.ndx')
				NDXfile.close()
				
				NDXfile = open(NDXfilenameCurrent,'w')
				NDXfile.write(NDXfileCurrent)
				NDXfile.close()
				
				#POSRES ########################################################
				sub.call('cp ../'+SampleToCopyName+'/*posres.itp .', shell= True)
			
			
			else:
				sub.call('cp ../'+SampleToCopyName+'/*.pdb .', shell= True)
				sub.call('cp ../'+SampleToCopyName+'/*.itp .', shell= True)
				sub.call('cp ../'+SampleToCopyName+'/*.ndx .', shell= True)
				sub.call('cp ../'+SampleToCopyName+'/*.top .', shell= True)
				
				PDBfilenameCurrent = SampleToCopyName+'.withbox.pdb'
				NDXfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.ndx')
				
			
				
				
		elif copyMethod == "all" :
			sub.call('cp ../'+SampleToCopyName+'/*.pdb .', shell= True)
			sub.call('cp ../'+SampleToCopyName+'/*.itp .', shell= True)
			sub.call('cp ../'+SampleToCopyName+'/*.ndx .', shell= True)
			sub.call('cp ../'+SampleToCopyName+'/*.top .', shell= True)
			
			PDBfilenameCurrent = SampleToCopyName+'.withbox.pdb'
			NDXfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.ndx')
	
	
	
	else:
		sub.call('cp ../'+SampleToCopyName+'/*.pdb .', shell= True)
		sub.call('cp ../'+SampleToCopyName+'/*.itp .', shell= True)
		sub.call('cp ../'+SampleToCopyName+'/*.ndx .', shell= True)
		sub.call('cp ../'+SampleToCopyName+'/*.top .', shell= True)
		
		PDBfilenameCurrent = SampleToCopyName+'.withbox.pdb'
		NDXfilenameCurrent = PDBfilenameCurrent.replace('.withbox.pdb','.ndx')
	
	System = PDBfilenameCurrent.strip('.withbox.pdb')
	return { 'SYSTEM': System, 'OUTPUT': PDBfilenameCurrent, 'INDEX':NDXfilenameCurrent}



def WriteMDP(Sample, step, defaultMDP, Version):
	
	# Get the parameters for the step
	stepMD = Sample['PROTOCOL'][step]
	
	if 'DEFO' in Sample:
		stepAfterInit = int(step)-1
		presetName = Sample['DEFO']['defoProtocol'][stepAfterInit].strip(' ')
		defoPresetForStep = Sample['DEFO']['presets'][presetName]
		
	if 'SU' in Sample:
		stepAfterInit = int(step)-1
		presetName = Sample['SU']['suProtocol'][stepAfterInit].strip(' ')
		suPresetForStep = Sample['SU']['presets'][presetName]
		SU_TYPE = Sample['SU']['SuType']
	
	#Showing the final parameters
	print("Writing step {0} ==========================".format(stepMD['stepType']))
	######for param in stepMD:
		######if param != 'stepType':
			######print(param +' = '+str(stepMD[param]))
	
	# Preparation with Parameters.csv before writing .mdp files ================
	
	#Bool to check that the run is of NVT or NPT type
	NPT_or_NVT = False
	
	#Look if the run is NPT or NVT
	if stepMD['stepType'].startswith('NPT') or stepMD['stepType'].startswith('NVT'):
		NPT_or_NVT = True
		# if THERMOSTAT is in Parameters.csv the values set here will override the values set
		# for NPT and NVT runs
		if 'THERMOSTAT' in Sample:
			if 'ref-t' in Sample['THERMOSTAT']:
				Sample['PROTOCOL'][step].update( {'ref-t': Sample['THERMOSTAT']['ref-t'] } )
	
	#Energy and Temperature groups
	Egrps = ''
	Tcgrps = ''
	# Multiply tau-t and ref-t by the number of grps
	Tau_Tcgrps = ''
	T_Tcgrps = ''
	autoEGrps = True
	autoTcGrps = True
	autoTau_TcGrps = True
	autoT_TcGrps = True
	#Creates grps for all lipid found except if tau-t and ref-t contain multiple values
	#Exception
	if 'energygrps' in Sample['PROTOCOL'][step]:
		if ' ' in str(Sample['PROTOCOL'][step]['energygrps']):
			Egrps += str(Sample['PROTOCOL'][step]['energygrps'])
			autoEGrps = False
			
	if 'tc-grps' in Sample['PROTOCOL'][step]:
		if ' ' in str(Sample['PROTOCOL'][step]['tc-grps']):
			Tcgrps += str(Sample['PROTOCOL'][step]['tc-grps'])
			autoTcGrps = False
			
	if 'tau-t' in Sample['PROTOCOL'][step]:
		if ' ' in str(Sample['PROTOCOL'][step]['tau-t']):
			Tau_Tcgrps += str(Sample['PROTOCOL'][step]['tau-t'])
			autoTau_TcGrps = False
			
	if 'ref-t' in Sample['PROTOCOL'][step]:
		if ' ' in str(Sample['PROTOCOL'][step]['ref-t']):
			T_Tcgrps += str(Sample['PROTOCOL'][step]['ref-t'])
			autoT_TcGrps = False
			
	#Automatic generation
	if autoEGrps or autoTcGrps or autoTau_TcGrps or autoT_TcGrps:
		for lipid in LipidsList:
			if lipid in Sample:
				if autoEGrps:
					Egrps += lipid+' '
				if(NPT_or_NVT):
					if autoTcGrps:
						Tcgrps += lipid+' '
					if autoTau_TcGrps:
						if 'tau-t' in Sample['PROTOCOL'][step] and autoTau_TcGrps:
							Tau_Tcgrps += str(Sample['PROTOCOL'][step]['tau-t'])+' '
						else:
							pass
					if autoT_TcGrps:
						if 'ref-t' in Sample['PROTOCOL'][step] and autoT_TcGrps:
							T_Tcgrps += str(Sample['PROTOCOL'][step]['ref-t'])+' '
						else:
							pass
					
		#Creates grps for all solvents found
		for sol in SolventsList:
			if sol in Sample:
				if autoEGrps:
					Egrps += sol+' '
				if NPT_or_NVT:
					if autoTcGrps:
						Tcgrps += sol+' '
						if 'tau-t' in Sample['PROTOCOL'][step] and autoTau_TcGrps:
							Tau_Tcgrps += str(Sample['PROTOCOL'][step]['tau-t'])+' '
						if 'ref-t' in Sample['PROTOCOL'][step] and autoT_TcGrps:
							T_Tcgrps += str(Sample['PROTOCOL'][step]['ref-t'])+' '
	
	#Updates the sample dictionnary with the values created above
	if(NPT_or_NVT):
		Sample['PROTOCOL'][step].update({ 'tc-grps': Tcgrps })
		Sample['PROTOCOL'][step].update({ 'tau-t': Tau_Tcgrps })
		Sample['PROTOCOL'][step].update({ 'ref-t': T_Tcgrps })
		
	#Creates grps for DEFO and modifies the parameters in .mdp if in the preset
	if 'DEFO' in Sample:
		defoMdpParams = '\n\n ;;; Parameters for Defo ;;; \n\n'
		Egrps += 'DEFO'
		if 'ref-t' in defoPresetForStep or 'tau-t' in defoPresetForStep: 
			Tcgrps += ' DEFO'
		
		for defoParam, defoParamValue in defoPresetForStep.items():
			if defoParam != 'posres':
				if defoParam in Sample['PROTOCOL'][step]:
					currValue = str(Sample['PROTOCOL'][step][defoParam])
					Sample['PROTOCOL'][step][defoParam] = currValue + ' ' + str(defoParamValue) + ' '
				else:
					defoMdpParams += defoParam + '		= '+ str(defoParamValue) + ' \n'
		
		if(NPT_or_NVT):
			Sample['PROTOCOL'][step].update({ 'tc-grps': Tcgrps })
	
	#Creates grps for SU and modifies the parameters in .mdp if in the preset
	if 'SU' in Sample:
		suMdpParams = '\n\n ;;; Parameters for Su ;;; \n\n'
		Egrps += ' '+ SU_TYPE
		if 'ref-t' in suPresetForStep or 'tau-t' in suPresetForStep: 
			Tcgrps += ' '+ SU_TYPE
		
		for suParam, suParamValue in suPresetForStep.items():
			if suParam != 'posres':
				if suParam in Sample['PROTOCOL'][step]:
					currValue = str(Sample['PROTOCOL'][step][suParam])
					Sample['PROTOCOL'][step][suParam] = currValue + ' ' + str(suParamValue) + ' '
				
				else:
					suMdpParams += suParam + '		= '+ str(suParamValue) + ' \n'
		
		if(NPT_or_NVT):
			Sample['PROTOCOL'][step].update({ 'tc-grps': Tcgrps })
			
	#Updates the Energy groups
	Sample['PROTOCOL'][step].update({ 'energygrps': Egrps })
	
	# End of preparation =======================================================
	
	
	
	# Beginning of writing .mdp ================================================
	
	#Looks for the parameters in Default MDP file and set the values
	#as chosen in Parameters.csv
	OUTPUT = open(stepMD['stepType']+'.mdp','w')
	
	#Position restraining for DEFO and Su if in preset
	
	if 'DEFO' in Sample and 'SU' not in Sample:
		if 'posres'  in defoPresetForStep:
			if defoPresetForStep['posres'] == 'on': OUTPUT.write("define = -DDEFO_POSRES")
			
	elif 'SU' in Sample and 'DEFO' not in Sample:
		if 'posres' in suPresetForStep:
			if suPresetForStep['posres'] == 'on': OUTPUT.write("define = -DSU_POSRES")
			
	elif 'SU' in Sample and 'DEFO' in Sample:
		if 'posres' in suPresetForStep and 'posres' in defoPresetForStep:
			if suPresetForStep['posres'] == 'on' and defoPresetForStep['posres'] == 'on' :
				OUTPUT.write("define = -DSU_POSRES -DDEFO_POSRES")
				
			elif suPresetForStep['posres'] == 'off' and defoPresetForStep['posres'] == 'on' :
				OUTPUT.write("define = -DDEFO_POSRES")
				
			elif suPresetForStep['posres'] == 'on' and defoPresetForStep['posres'] == 'off' :
				OUTPUT.write("define = -DSU_POSRES")
				
				
	
		
	CopyOriginalLine = True
	for i, line in enumerate(defaultMDP):
		if not line.startswith(';'):
			for key in stepMD:
				if key in line and key != '' and (line.partition(' ')[0] == key or line.partition('=')[0] == key):
					OUTPUT.write(key+'			= '+ str(stepMD[key])+'\n')
					CopyOriginalLine = False
					continue
			if(CopyOriginalLine):
				OUTPUT.write(line)
			CopyOriginalLine=True

	OUTPUT = open(stepMD['stepType']+'.mdp','a+')
	OUTPUT.write('\n ;Parameters not in default file : \n\n')
	
	# Open the file again to add the parameters not in default MDP
	COMPARE = open(stepMD['stepType']+'.mdp','r').read()
	for key in stepMD:
		if key not in COMPARE and key != 'stepType':
			OUTPUT.write(key+'			= '+ str(stepMD[key])+'\n')
	
	# Writes parameters related to Defo at the end
	if 'DEFO' in Sample:
		OUTPUT.write(defoMdpParams)
	
	# Options if DEFO
	if 'DEFO' in Sample and Sample['TYPE'] == 'BILAYER' and 'SU' not in Sample:
		if Version.startswith('4'):
			#finding current lipid used
			Lipid = ''
			for lipid in LipidsList:
				if lipid in Sample:
					Lipid = lipid
			OUTPUT.write('pull-group1		= {0}\n'.format(Lipid))
		else:
			#finding current lipid used
			Lipid = ''
			for lipid in LipidsList:
				if lipid in Sample:
					Lipid = lipid
			OUTPUT.write('pull-group1-name		= {0}\n'.format(Lipid))
		
	# Writes parameters related to Su at the end
	if 'SU' in Sample:
		OUTPUT.write(suMdpParams)
	
	
	defaultMDP.seek(0)

	OUTPUT.close()
