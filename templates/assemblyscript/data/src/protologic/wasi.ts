// DO NOT MODIFY, THIS FILE IS GENERATED //
// VERSION 0.2.0 //



// wasi.ts


// @ts-ignore
@external("wasi_snapshot_preview1", "sched_yield")
declare function _internal_sched_yield(): i32;

/**
 */
export function sched_yield(): i32 {
	return _internal_sched_yield();
}

