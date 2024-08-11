# backup from https://gist.github.com/fjes/cdcaf5bf11bb453f02ce
# calculate BRP, T_ps1 and T_ps2 for the MCP2515

def TQ(brp, Fosc):
        return float(2*brp)/Fosc

def TQBit(fbaud, tq):
        return 1/(float(fbaud*tq))

# ------

# Constants

Fosc = 8000000        # 8 MHz
Tosc = 1/float(Fosc)

Fbaud = [ 50000, 100000, 125000, 250000, 500000, 1000000 ] # kHz bit rate

baudrate = 125000 # kHz

# bit time sections in quantities of time quantas (TQ)
t_syncseg   = 1    # fixed
t_propseg   = 2    # fixed, min=1 max=8
t_ps1       = 1    # min=1 max=8
t_ps2       = 2    # min=2 max=8
SJW         = 1    # fixed

SamplePoint = 70   # percent

# -----

print ("MCP2515 Settings:")
print ("BTLMODE = 1")

for brp in [1, 2, 3, 4, 5, 10, 15, 20, 30, 50 ]:
        for b in Fbaud:
                tqall = TQBit(b, TQ(brp, 8000000))
                tq70 = tqall * 0.75
                t_ps1 = tq70 - ( t_syncseg + t_propseg )
                t_ps2 = tqall - t_ps1

                if (t_ps1 < 1 or t_ps1 > 8 or t_ps2 < 2):
                        continue

                if ((t_propseg + t_ps1) < t_ps2):
                        continue
                if (t_ps2 <= SJW):
                        continue


                print ("Fbaud = %dkHz; tqall = %d; tq70 = %d; BRP = %d; t_ps1 = %d; t_ps2 = %d" % (b/1000, tqall, tq70, brp, t_ps1, t_ps2))