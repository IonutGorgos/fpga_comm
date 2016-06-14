import pico

ps = pico.PICO()
ps.open()
print("Attempting to open Picoscope 6000...")
ps.parameters(2 * 1E-6, 3.2 * 1E-9)
# ps.get_samples(2*1E-6,3.2*1E-9)
ps.get_samples()
ps.trigger('B', 0.0, 'Falling', 100, True)
ps.arm(10, 0.5, 16, 2, 'test_', 'A', 'B', chNum3='C', chCoupling='DC',
       chVRange1=50E-3, chVRange2=500E-3, chVRange3=50E-3, enabled1=True,
       enabled2=True, enabled3=False, BWLimited1=2, BWLimited2=0, BWLimited3=0)
print("Attempting to close Picoscope 6000...")
ps.close()
