
#include <complex.h>
#include <stdbool.h>

struct signal_model {
	
	float m0;
	float m0_water;
	float m0_fat;
	float t1;
	float t2;
	float t2star;
	float te;
	float tr;
	float b0;
	float off_reson;
	float fa;
	float beta;
	bool ir;
	bool ir_ss;
};


extern const struct signal_model signal_TSE_defaults;

extern void TSE_model(const struct signal_model* data, int N, complex float out[N]);


extern const struct signal_model signal_hsfp_defaults;

extern void hsfp_simu(const struct signal_model* data, int N, const float pa[N], complex float out[N]);


extern const struct signal_model signal_looklocker_defaults;

extern void looklocker_model(const struct signal_model* data, int N, complex float out[N]);

extern void MOLLI_model(const struct signal_model* data, int N, int Hbeats, float time_T1relax, complex float out[N]);


extern const struct signal_model signal_IR_bSSFP_defaults;

extern void IR_bSSFP_model(const struct signal_model* data, int N, complex float out[N]);


extern const struct signal_model signal_multi_grad_echo_defaults;

extern complex float calc_fat_modulation(float b0, float TE);

extern void multi_grad_echo_model(const struct signal_model* data, int N, complex float out[N]);

